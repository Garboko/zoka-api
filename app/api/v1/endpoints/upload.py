from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi.responses import StreamingResponse
from io import BytesIO
import logging

from app.database.session import get_db
from app.services.storage import storage_service
from app.services.xlsform import xlsform_service
from app.crud import forms as crud_forms
from app.schemas.forms import FormCreate, FormResponse
from app.core.dependencies import get_current_active_user
from app.models.users import User
from app.middleware.rate_limit import limiter

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/xlsform", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")  
async def upload_xlsform(
    request: Request,
    title: str,
    project_id: str = None,
    description: str = None,
    public_access: bool = False,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        logger.warning(f"⚠️ Invalid file type attempted: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    file_data = await file.read()
    if len(file_data) > MAX_FILE_SIZE:
        logger.warning(f"File too large: {len(file_data)} bytes (max: {MAX_FILE_SIZE})")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
        )
    
    logger.info(f"Uploading XLSForm: {file.filename} ({len(file_data)} bytes)")
    
    is_valid, error_msg = xlsform_service.validate_xlsform(file_data)
    if not is_valid:
        logger.warning(f"Invalid XLSForm: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid XLSForm: {error_msg}"
        )
    
    form_id = str(uuid4())
    xlsform_path = f"forms/{form_id}/{file.filename}"
    xform_path = f"xforms/{form_id}/{form_id}.xml"
    
    try:
        storage_service.upload_file(
            file_data,
            xlsform_path,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        xml_content, error_msg = xlsform_service.convert_xlsform_to_xform(file_data, form_id)
        if not xml_content:
            storage_service.delete_file(xlsform_path)
            logger.error(f"XForm conversion failed: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error converting XLSForm: {error_msg}"
            )
        
        storage_service.upload_file(
            xml_content.encode('utf-8'),
            xform_path,
            content_type="application/xml"
        )
        
        form_create = FormCreate(
            user_id=current_user.id,
            project_id=project_id,
            title=title,
            description=description,
            original_file=xlsform_path,
            converted_file=xform_path,
            public_access=public_access
        )
        
        form = crud_forms.create(db, obj_in=form_create)
        db.commit()  
        
        logger.info(f"Form created successfully: {form.id} - {title}")
        return form
        
    except HTTPException:
        raise
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error during XLSForm upload: {e}", exc_info=True)
        
        try:
            storage_service.delete_file(xlsform_path)
            storage_service.delete_file(xform_path)
        except Exception as cleanup_error:
            logger.error(f"Error during cleanup: {cleanup_error}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload form. Please try again."
        )

@router.post("/media/{submission_id}")
@limiter.limit("20/hour")  
async def upload_media(
    request: Request,
    submission_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
    from app.crud import submissions as crud_submissions
    from app.crud import forms as crud_forms
    from app.crud import media_files as crud_media_files
    from app.schemas.media_files import MediaFileCreate
    
    submission = crud_submissions.get(db, id=submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    form = crud_forms.get(db, id=submission.form_id)
    if form.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    file_data = await file.read()
    if len(file_data) > MAX_FILE_SIZE:
        logger.warning(f"⚠️ Media file too large: {len(file_data)} bytes")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
        )
    
    logger.info(f"📤 Uploading media: {file.filename} ({len(file_data)} bytes)")
    
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
    unique_filename = f"{uuid4()}.{file_extension}" if file_extension else str(uuid4())
    media_path = f"media/{submission_id}/{unique_filename}"
    
    try:
        storage_service.upload_file(
            file_data,
            media_path,
            content_type=file.content_type or "application/octet-stream"
        )
        
        media_file_create = MediaFileCreate(
            submission_id=submission_id,
            file_path=media_path,
            file_type=file.content_type
        )
        
        media_file = crud_media_files.create(db, obj_in=media_file_create)
        db.commit()  
        
        logger.info(f"Media file uploaded: {media_file.id}")
        
        return {
            "id": media_file.id,
            "file_path": media_path,
            "file_url": storage_service.get_file_url(media_path)
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading media: {e}", exc_info=True)
        
        try:
            storage_service.delete_file(media_path)
        except Exception as cleanup_error:
            logger.error(f"Error during cleanup: {cleanup_error}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload media file. Please try again."
        )

@router.get("/download/{path:path}")
async def download_file(
    path: str,
    current_user: User = Depends(get_current_active_user)
):
    
    try:
        if not storage_service.file_exists(path):
            logger.warning(f"File not found: {path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        file_data = storage_service.download_file(path)
        
        content_type_map = {
            '.xlsx': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            '.xls': "application/vnd.ms-excel",
            '.xml': "application/xml",
            '.jpg': "image/jpeg",
            '.jpeg': "image/jpeg",
            '.png': "image/png",
            '.pdf': "application/pdf",
            '.csv': "text/csv",
        }
        
        file_extension = '.' + path.split('.')[-1].lower() if '.' in path else ''
        content_type = content_type_map.get(file_extension, "application/octet-stream")
        
        filename = path.split('/')[-1]
        
        logger.info(f"📥 File downloaded: {path}")
        
        return StreamingResponse(
            BytesIO(file_data),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file {path}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file."
        )
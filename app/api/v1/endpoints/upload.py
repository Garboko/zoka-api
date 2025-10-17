from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database.session import get_db
from app.services.storage import storage_service
from app.services.xlsform import xlsform_service
from app.crud import forms as crud_forms
from app.schemas.forms import FormCreate, FormResponse
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/xlsform", response_model=FormResponse, status_code=status.HTTP_201_CREATED)
async def upload_xlsform(
    title: str,
    project_id: str = None,
    description: str = None,
    public_access: bool = False,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    file_data = await file.read()
    
    is_valid, error_msg = xlsform_service.validate_xlsform(file_data)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid XLSForm: {error_msg}"
        )
    
    form_id = str(uuid4())
    
    xlsform_path = f"forms/{form_id}/{file.filename}"
    try:
        storage_service.upload_file(
            file_data,
            xlsform_path,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
    
    xml_content, error_msg = xlsform_service.convert_xlsform_to_xform(file_data, form_id)
    if not xml_content:
        storage_service.delete_file(xlsform_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error converting XLSForm to XForm: {error_msg}"
        )
    
    xform_filename = f"{form_id}.xml"
    xform_path = f"xforms/{form_id}/{xform_filename}"
    try:
        storage_service.upload_file(
            xml_content.encode('utf-8'),
            xform_path,
            content_type="application/xml"
        )
    except Exception as e:
        storage_service.delete_file(xlsform_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading XForm: {str(e)}"
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
    
    return form

@router.post("/media/{submission_id}")
async def upload_media(
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
    
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    media_path = f"media/{submission_id}/{unique_filename}"
    
    try:
        storage_service.upload_file(
            file_data,
            media_path,
            content_type=file.content_type or "application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading media: {str(e)}"
        )
    
    media_file_create = MediaFileCreate(
        submission_id=submission_id,
        file_path=media_path,
        file_type=file.content_type
    )
    
    media_file = crud_media_files.create(db, obj_in=media_file_create)
    
    return {
        "id": media_file.id,
        "file_path": media_path,
        "file_url": storage_service.get_file_url(media_path)
    }

@router.get("/download/{bucket}/{path:path}")
async def download_file(
    bucket: str,
    path: str,
    current_user: User = Depends(get_current_active_user)
):
    object_name = f"{path}"
    
    if not storage_service.file_exists(object_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    url = storage_service.get_file_url(object_name, expires=3600)
    
    return {"download_url": url}
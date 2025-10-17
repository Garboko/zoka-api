from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from fastapi.responses import Response, StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from io import BytesIO
import secrets

from app.database.session import get_db
from app.crud import enumerators as crud_enumerators
from app.crud import forms as crud_forms
from app.crud import form_access as crud_form_access
from app.crud import submissions as crud_submissions
from app.crud import media_files as crud_media_files
from app.services.storage import storage_service
from app.schemas.submissions import SubmissionCreate
from app.schemas.media_files import MediaFileCreate
from app.core.security import verify_password
from uuid import uuid4

router = APIRouter()
security = HTTPBasic()

def authenticate_enumerator(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    enumerator = crud_enumerators.get_by_email(db, email=credentials.username)
    
    if not enumerator:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if not enumerator.password_hash or not verify_password(credentials.password, enumerator.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if not enumerator.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive enumerator"
        )
    
    return enumerator

@router.get("/formList")
async def form_list(
    request: Request,
    enumerator = Depends(authenticate_enumerator),
    db: Session = Depends(get_db)
):
    form_accesses = crud_form_access.get_by_enumerator(db, enumerator_id=enumerator.id)
    
    base_url = str(request.base_url).rstrip('/')
    
    forms_xml = []
    for access in form_accesses:
        form = crud_forms.get(db, id=access.form_id)
        if form and form.converted_file:
            form_id = form.id
            download_url = f"{base_url}/api/v1/openrosa/forms/{form_id}.xml"
            
            forms_xml.append(f"""
    <xform>
        <formID>{form_id}</formID>
        <name>{form.title}</name>
        <version>{form.version}</version>
        <hash>md5:{form_id}</hash>
        <downloadUrl>{download_url}</downloadUrl>
    </xform>""")
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <xforms xmlns="http://openrosa.org/xforms/xformsList">
                        {''.join(forms_xml)}
                    </xforms>"""
    
    return Response(
        content=xml_response,
        media_type="text/xml",
        headers={
            "X-OpenRosa-Version": "1.0",
            "X-OpenRosa-Accept-Content-Length": "10485760"
        }
    )

@router.get("/forms/{form_id}.xml")
async def download_xform(
    form_id: str,
    enumerator = Depends(authenticate_enumerator),
    db: Session = Depends(get_db)
):
    form_access = crud_form_access.get_by_enumerator_and_form(
        db, enumerator_id=enumerator.id, form_id=form_id
    )
    
    if not form_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this form"
        )
    
    form = crud_forms.get(db, id=form_id)
    if not form or not form.converted_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )
    
    try:
        xml_data = storage_service.download_file(form.converted_file)
        
        return Response(
            content=xml_data,
            media_type="text/xml",
            headers={
                "X-OpenRosa-Version": "1.0",
                "Content-Disposition": f"attachment; filename={form_id}.xml"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading form: {str(e)}"
        )

@router.post("/submission")
async def submit_data(
    xml_submission_file: UploadFile = File(...),
    enumerator = Depends(authenticate_enumerator),
    db: Session = Depends(get_db)
):
    try:
        xml_content = await xml_submission_file.read()
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_content)
        
        form_id = root.get('id')
        
        if not form_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Form ID not found in submission"
            )
        
        form_access = crud_form_access.get_by_enumerator_and_form(
            db, enumerator_id=enumerator.id, form_id=form_id
        )
        
        if not form_access or not form_access.can_submit:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to submit to this form"
            )
        
        submission_data = {}
        for child in root:
            tag = child.tag.split('}')[-1]  
            submission_data[tag] = child.text
        
        submission_create = SubmissionCreate(
            form_id=form_id,
            enumerator_id=enumerator.id,
            submission_data=submission_data
        )
        
        submission = crud_submissions.create(db, obj_in=submission_create)
        
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <OpenRosaResponse xmlns="http://openrosa.org/http/response">
                            <message>Success</message>
                            <submissionMetadata xmlns="http://www.opendatakit.org/xforms" id="{submission.id}" submissionDate="{submission.submitted_at.isoformat()}Z"/>
                        </OpenRosaResponse>"""
        
        return Response(
            content=response_xml,
            media_type="text/xml",
            status_code=status.HTTP_201_CREATED,
            headers={
                "X-OpenRosa-Version": "1.0",
                "X-OpenRosa-Accept-Content-Length": "10485760",
                "Location": f"/api/v1/openrosa/submission/{submission.id}"
            }
        )
        
    except ET.ParseError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid XML: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing submission: {str(e)}"
        )

@router.post("/submission/{submission_id}/attachments")
async def upload_attachment(
    submission_id: str,
    file: UploadFile = File(...),
    enumerator = Depends(authenticate_enumerator),
    db: Session = Depends(get_db)
):
    submission = crud_submissions.get(db, id=submission_id)
    
    if not submission or submission.enumerator_id != enumerator.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this submission"
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
    
    return Response(
        content="File uploaded successfully",
        status_code=status.HTTP_201_CREATED,
        headers={
            "X-OpenRosa-Version": "1.0"
        }
    )

@router.head("/")
async def openrosa_head():
    """
    OpenRosa discovery endpoint
    """
    return Response(
        headers={
            "X-OpenRosa-Version": "1.0",
            "X-OpenRosa-Accept-Content-Length": "10485760"
        }
    )
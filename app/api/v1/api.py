from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, projects, forms, submissions,
    enumerators, form_access, devices, form_versions,
    submission_reviews, media_files, audit_logs
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(enumerators.router, prefix="/enumerators", tags=["enumerators"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(form_access.router, prefix="/form-access", tags=["form-access"])
api_router.include_router(form_versions.router, prefix="/form-versions", tags=["form-versions"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
api_router.include_router(submission_reviews.router, prefix="/submission-reviews", tags=["submission-reviews"])
api_router.include_router(media_files.router, prefix="/media-files", tags=["media-files"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
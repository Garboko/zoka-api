from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, projects, forms, submissions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
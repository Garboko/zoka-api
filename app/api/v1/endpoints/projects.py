from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate
from app.crud import projects as crud_projects
from app.core.dependencies import get_current_active_user
from app.models.users import User

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project_in.user_id = current_user.id
    project = crud_projects.create(db, obj_in=project_in)
    return project

@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    projects = crud_projects.get_by_user_id(db, user_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = crud_projects.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = crud_projects.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    project = crud_projects.update(db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = crud_projects.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    crud_projects.delete(db, id=project_id)
    return {"message": "Project deleted successfully"}
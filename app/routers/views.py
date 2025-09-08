from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.crud.projects import (create_project,
                               get_user_projects,
                               get_project_by_id,
                               update_project,
                               delete_project)

router = APIRouter(tags=["views"])

@router.post("/projects")
def project_creation(project: ProjectCreate,
                   user_id: int = Depends(get_current_user_id),
                   conn = Depends(get_db)):
    db_project = create_project(conn, project.name, project.description, user_id)

    return {
        "return_code": status.HTTP_201_CREATED,
        "message": "Project created",
        "project": db_project
    }

@router.get("/projects")
def list_projects(user_id: int = Depends(get_current_user_id),
                  conn = Depends(get_db)):
    projects = get_user_projects(conn, user_id)
    return {
        "status_code": status.HTTP_200_OK,
        "projects": projects
    }

@router.get("/projects/{project_id}/info")
def get_project_info(project_id: int,
                     user_id: int = Depends(get_current_user_id),
                     conn = Depends(get_db)):
    project = get_project_by_id(conn, project_id, user_id)
    if not project:
        raise HTTPException(404, "Project not found or no access")
    return {
        "status_code": status.HTTP_200_OK,
        "project": project
    }

@router.put("/projects/{project_id}/info")
def update_project_info(
    project_id: int,
    data: ProjectUpdate,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    project = get_project_by_id(conn, project_id, user_id)
    if not project:
        raise HTTPException(404, "Project not found or no access")

    updated = update_project(conn, project_id, data.name, data.description)
    if not updated:
        raise HTTPException(500, "Failed to update project")
    return {
        "status_code": status.HTTP_200_OK,
        "updated": updated
    }

@router.delete("/projects/{project_id}")
def delete_project_endpoint(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    success = delete_project(conn, project_id, user_id)
    if not success:
        raise HTTPException(403, "Only the owner can delete this project")
    return {
        "status_code": status.HTTP_200_OK,
        "message": "Project deleted"
    }
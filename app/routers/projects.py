from fastapi import APIRouter, status, HTTPException, UploadFile, File, Query
from fastapi.params import Depends

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.crud.projects import (create_project,
                               get_user_projects,
                               get_project_by_id,
                               update_project,
                               delete_project,
                               get_project_role,
                               get_user_by_username,
                               add_user_to_project,)

router = APIRouter(tags=["projects"])

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

@router.post("/project/{project_id}/invite")
def invite_user_to_project(
    project_id: int,
    user: str = Query(..., alias="user"),
    current_user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    role = get_project_role(conn, project_id, current_user_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found or no access")
    if role != "owner":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the owner can invite users")

    target_user = get_user_by_username(conn, user)
    if not target_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    target_user_id = target_user["user_id"]

    if target_user_id == current_user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You cannot invite yourself")

    success = add_user_to_project(conn, project_id, target_user_id, "participant")
    if not success:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is already in the project")

    return {
        "status_code": status.HTTP_200_OK,
        "message": "User invited successfully",
        "project_id": project_id,
        "username": target_user["username"],
        "role": "participant"
    }
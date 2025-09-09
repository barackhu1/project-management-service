from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.params import Depends

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.crud.projects import (create_project,
                               get_user_projects,
                               get_project_by_id,
                               update_project,
                               delete_project,
                               create_document,
                               user_has_access_to_project,
                               get_documents_by_project,)

router = APIRouter(tags=["views"])

UPLOADS_PATH = "../uploads/"

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

@router.post("/project/{project_id}/documents")
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    if not user_has_access_to_project(conn, project_id, user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found or no access")

    file_location = f"{UPLOADS_PATH}/{project_id}_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    doc = create_document(conn, project_id, file.filename, file_location, user_id)

    return {"status_code": status.HTTP_201_CREATED,
            "message": "File uploaded",
            "document": doc}

@router.get("/project/{project_id}/documents")
def list_documents(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    documents = get_documents_by_project(conn, project_id, user_id)
    if documents is None:
        raise HTTPException(404, "Project not found or no access")
    return {"documents": documents}
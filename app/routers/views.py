from fastapi import APIRouter, status
from fastapi.params import Depends

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db
from app.schemas.schemas import ProjectCreate
from app.crud.projects import create_project, get_user_projects

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
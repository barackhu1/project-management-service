from fastapi import APIRouter
from fastapi.params import Depends

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db
from app.schemas.schemas import ProjectCreate

router = APIRouter(tags=["views"])

@router.post("/projects")
def create_project(project: ProjectCreate,
                   user_id: int = Depends(get_current_user_id),
                   conn = Depends(get_db)):
    pass
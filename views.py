from fastapi import APIRouter

router = APIRouter(tags=["views"])

@router.get("/")
def root():
    return {"message": "FastAPI is running!"}
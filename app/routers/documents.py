import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.utils.auth_dependency import get_current_user_id
from app.utils.db import get_db, user_has_access_to_project
from app.crud.documents import (create_document,
                                get_documents_by_project,
                                get_document_by_id,
                                update_document_file,
                                delete_document,)

router = APIRouter(tags=["documents"])

UPLOADS_PATH = "../uploads"

@router.post("/project/{project_id}/documents")
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    if not user_has_access_to_project(conn, project_id, user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found or no access")

    filename = os.path.splitext(file.filename)[0]
    file_extension = os.path.splitext(file.filename)[1]
    unique_id = str(uuid.uuid4())[:8]
    file_location = f"{UPLOADS_PATH}/{project_id}_{filename}_{unique_id}{file_extension}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    doc = create_document(conn, project_id, file.filename, file_location, user_id)

    return {
        "status_code": status.HTTP_201_CREATED,
        "message": "File uploaded",
        "document": doc
    }

@router.get("/project/{project_id}/documents")
def list_documents(
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    documents = get_documents_by_project(conn, project_id, user_id)
    if documents is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Project not found or no access")

    return {
        "status_code": status.HTTP_200_OK,
        "documents": documents
    }

@router.get("/document/{document_id}")
def download_document(
    document_id: int,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    document = get_document_by_id(conn, document_id, user_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or no access to project"
        )
    file_path = document["file_path"]

    return FileResponse(
        path=file_path,
        filename=document["filename"],
        media_type="application/octet-stream"
    )

@router.put("/document/{document_id}")
async def update_document(
    document_id: int,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    document = get_document_by_id(conn, document_id, user_id)
    if not document:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found or no access to project")

    project_id = document["project_id"]
    old_file_path = document["file_path"]
    file_location = f"{UPLOADS_PATH}/{project_id}_{file.filename}"

    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to save file: {str(e)}")

    updated_doc = update_document_file(conn, document_id, file.filename, file_location, user_id)
    if not updated_doc:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update document in database")

    if os.path.exists(old_file_path) and old_file_path != file_location:
        os.remove(old_file_path)

    return {
        "status_code": status.HTTP_200_OK,
        "message": "Document updated successfully",
        "document": updated_doc
    }

@router.delete("/document/{document_id}")
def delete_document_endpoint(
    document_id: int,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_db)
):
    file_path = delete_document(conn, document_id, user_id)
    if not file_path:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found or no access to project")

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            pass
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to delete file from disk: {str(e)}")

    return {
        "status_code": status.HTTP_200_OK,
        "message": "Document deleted successfully"
    }
from app.utils.db import user_has_access_to_project

def create_document(conn, project_id: int, filename: str, file_path: str, uploaded_by: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (project_id, filename, file_path, uploaded_by)
            VALUES (%s, %s, %s, %s)
            RETURNING document_id, filename, file_path, uploaded_by, uploaded_at
            """,
            (project_id, filename, file_path, uploaded_by)
        )
        doc = cur.fetchone()
        conn.commit()
        return dict(doc)

def get_documents_by_project(conn, project_id: int, user_id: int):
    if not user_has_access_to_project(conn, project_id, user_id):
        return None

    with conn.cursor() as cur:
        cur.execute("""
            SELECT document_id, filename, file_path, uploaded_by, uploaded_at
            FROM documents
            WHERE project_id = %s
            ORDER BY uploaded_at DESC
        """, (project_id,))
        return [dict(row) for row in cur.fetchall()]
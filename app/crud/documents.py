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

def get_document_by_id(conn, document_id: int, user_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT d.document_id, d.filename, d.file_path, d.project_id, d.uploaded_by, d.uploaded_at
            FROM documents d
            JOIN project_access pa ON d.project_id = pa.project_id
            WHERE d.document_id = %s AND pa.user_id = %s
        """, (document_id, user_id))
        row = cur.fetchone()
        return dict(row) if row else None

def update_document_file(conn, document_id: int,
                         filename: str,
                         file_path: str,
                         uploaded_by: int):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE documents
            SET filename = %s,
                file_path = %s,
                uploaded_by = %s,
                uploaded_at = NOW()
            WHERE document_id = %s
            RETURNING document_id, filename, file_path, project_id, uploaded_by, uploaded_at
        """, (filename, file_path, uploaded_by, document_id))
        doc = cur.fetchone()
        conn.commit()
        return dict(doc) if doc else None
def create_project(conn, name: str, description: str, owner_id: int):
    with conn.cursor() as cur:
        # Insert project
        cur.execute(
            """
            INSERT INTO projects (name, description, owner_id)
            VALUES (%s, %s, %s)
            RETURNING project_id, name, description, owner_id, created_at
            """,
            (name, description, owner_id)
        )
        project = cur.fetchone()

        # Grant owner access
        cur.execute(
            "INSERT INTO project_access (project_id, user_id, role) VALUES (%s, %s, 'owner')",
            (project['project_id'], owner_id)
        )
        conn.commit()

        return dict(project)

def get_user_projects(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.project_id, p.name, p.description, p.owner_id, p.created_at, pa.role
            FROM projects p
            JOIN project_access pa ON p.project_id = pa.project_id
            WHERE pa.user_id = %s
            ORDER BY p.created_at DESC
        """, (user_id,))
        return [dict(row) for row in cur.fetchall()]

def get_project_by_id(conn, project_id: int, user_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.project_id, p.name, p.description, p.owner_id, p.created_at, pa.role
            FROM projects p
            JOIN project_access pa ON p.project_id = pa.project_id
            WHERE p.project_id = %s AND pa.user_id = %s
        """, (project_id, user_id))
        row = cur.fetchone()
        return dict(row) if row else None

def update_project(conn, project_id: int, name: str, description: str):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE projects
            SET name = %s, description = %s
            WHERE project_id = %s
            RETURNING project_id, name, description, owner_id, created_at
        """, (name, description, project_id))
        project = cur.fetchone()
        conn.commit()
        return dict(project) if project else None

def user_has_access_to_project(conn, project_id: int, user_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1 FROM project_access
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        return cur.fetchone() is not None

def delete_project(conn, project_id: int, user_id: int):
    with conn.cursor() as cur:
        if not user_has_access_to_project(conn, project_id, user_id):
            return None

        cur.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
        conn.commit()
        return True

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
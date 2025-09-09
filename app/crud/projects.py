import os

from app.utils.db import user_has_access_to_project

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

def delete_project(conn, project_id: int, user_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1 FROM project_access
            WHERE project_id = %s AND user_id = %s AND role = 'owner'
        """, (project_id, user_id))
        if not cur.fetchone():
            return False

        cur.execute("SELECT file_path FROM documents WHERE project_id = %s", (project_id,))
        file_paths = [row["file_path"] for row in cur.fetchall()]

        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete file {file_path}: {str(e)}")

        cur.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
        conn.commit()
        return True

def get_project_role(conn, project_id: int, user_id: int) -> str:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT role FROM project_access
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        row = cur.fetchone()
        return row["role"] if row else None

def get_user_by_username(conn, username: str):
    with conn.cursor() as cur:
        cur.execute("SELECT user_id, username FROM users WHERE username = %s", (username,))
        return cur.fetchone()

def add_user_to_project(conn, project_id: int, user_id: int, role: str = "participant"):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO project_access (project_id, user_id, role) VALUES (%s, %s, %s)",
            (project_id, user_id, role)
        )
        conn.commit()
        return True

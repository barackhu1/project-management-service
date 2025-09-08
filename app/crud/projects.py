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
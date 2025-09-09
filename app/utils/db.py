import psycopg2
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2._psycopg import connection
from typing import Any, Generator

from psycopg2.extras import DictCursor

from app.config import (DB_NAME,
                    DB_USER,
                    DB_PASSWORD,
                    DB_HOST)

load_dotenv()

def get_db() -> Generator[connection, Any, None]:
    conn = connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
    )
    conn.cursor_factory = DictCursor
    try:
        yield conn
    finally:
        conn.close()

def user_has_access_to_project(conn, project_id: int, user_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1 FROM project_access
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        return cur.fetchone() is not None
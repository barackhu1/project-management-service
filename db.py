from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2._psycopg import connection
from typing import Any, Generator

from config import (DB_NAME,
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
    try:
        yield conn
    finally:
        conn.close()
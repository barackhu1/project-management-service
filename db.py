import os

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2._psycopg import connection
from typing import Any, Generator

load_dotenv()

def get_db() -> Generator[connection, Any, None]:
    conn = connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
    )
    try:
        yield conn
    finally:
        conn.close()
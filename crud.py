import psycopg2.extras

def cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def insert_user(conn, user_data):
    with cursor(conn) as cur:
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', user_data)
    conn.commit()
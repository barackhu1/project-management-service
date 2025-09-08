def insert_user(conn, username, hashed_password):
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id, username",
                (username, hashed_password)
            )
            result = cur.fetchone()
            conn.commit()
            return {"user_id": result[0], "username": result[1]}
        except Exception as e:
            conn.rollback()
            raise e

def get_user_by_username(conn, username):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        return cur.fetchone()

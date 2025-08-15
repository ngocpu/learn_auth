class TokenQueries:
    save_token = """
        INSERT INTO refresh_token(user_id, token, expires_at, created_at) VALUES (%s, %s,%s, %s)
        RETURNING *;
    """,
    get_valid_token = """
        SELECT * FROM refresh_token WHERE token = %s AND expires_at > NOW()
        RETURNING *;
    """,
    revoke_token = """
        DELETE FROM refresh_token WHERE token = %s;
    """
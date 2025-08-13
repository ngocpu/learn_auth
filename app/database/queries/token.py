class TokenQueries:
    save_token = """
        INSERT INTO refresh_token(user_id, token, expires_at, created_at) VALUES (%s, %s,%s, %s)
        RETURNING *;
    """
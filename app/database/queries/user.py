class UserQueries:
    get_user_by_id = """
    SELECT * FROM users WHERE id = %s
    """

    get_user_by_username = """
    SELECT * FROM users WHERE username = %s
    """

    get_user_by_email = """
    SELECT * FROM users WHERE email = %s
    """

    get_user_by_provider_id = """
    SELECT * FROM users WHERE provider_id = %s AND provider = %s
    """

    get_all_users = """
    SELECT * FROM users
    """

    create_user = """
    INSERT INTO users (username, email, password, provider_id, provider, avatar, activate)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING *
    """

    update_user = """
    UPDATE users SET username = %s, email = %s, password = %s, provider_id = %s, provider = %s, avatar = %s, activate = %s
    WHERE id = %s
    RETURNING *
    """

    delete_user = """
    DELETE FROM users WHERE id = %s
    RETURNING *
    """

    activate_user = """
    UPDATE users SET activate = TRUE WHERE id = %s RETURNING *
    """

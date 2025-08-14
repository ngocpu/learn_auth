class OTPQueries:
    save_otp = """
    INSERT INTO opt_code (user_id, code, expires_at, is_used, created_at)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *;
    """

    get_otp_by_user_id = """
    SELECT * FROM opt_code WHERE user_id = %s ORDER BY created_at DESC LIMIT 1
    """

    get_otp_by_code = """
    SELECT * FROM opt_code WHERE code = %s AND user_id = %s AND is_used = FALSE AND expires_at > NOW() AT TIME ZONE 'UTC'
    """

    mark_otp_as_used = """
    UPDATE opt_code SET is_used = TRUE WHERE id = %s
    RETURNING *
    """

    delete_expired_otps = """
    DELETE FROM opt_code WHERE expires_at < NOW()
    """
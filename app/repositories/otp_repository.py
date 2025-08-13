from datetime import datetime
from typing import Optional, List
from app.models.user import OTP
from app.database import execute_query, OTPQueries

class OTPRepositories:
    def save_otp_code(self, user_id: int, code: str, expires_at: datetime) -> OTP:
        row = execute_query(
            OTPQueries.save_otp,
            (user_id, code, expires_at, False, datetime.now())
        )
        return OTP(**row)

    def get_latest_otp_by_user_id(self, user_id: int) -> Optional[OTP]:
        row = execute_query(OTPQueries.get_otp_by_user_id, (user_id,))
        return OTP(**row) if row else None

    def get_verified_otp(self, user_id: int, code: str) -> Optional[OTP]:
        row = execute_query(
            OTPQueries.get_otp_by_code,
            (code, user_id)
        )
        return OTP(**row) if row else None

    def mark_otp_as_used(self, otp_id: int) -> OTP:
        row = execute_query(
            OTPQueries.mark_otp_as_used,
            (otp_id,)
        )
        return OTP(**row)

    def delete_expired_otps(self) -> int:
        return execute_query(OTPQueries.delete_expired_otps, ())

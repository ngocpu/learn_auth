from datetime import datetime
from typing import Optional, List
from app.models.user import OTP
from app.database import execute_query, OTPQueries
import asyncio

class OTPRepositories:
    async def save_otp_code(self, user_id: int, code: str, expires_at: datetime, conn=None) -> OTP:
        row = await asyncio.to_thread(
            execute_query,
            OTPQueries.save_otp,
            (user_id, code, expires_at, False, datetime.now()),
            conn=conn
        )
        return OTP(**row)

    async def get_latest_otp_by_user_id(self, user_id: int, conn=None) -> Optional[OTP]:
        row = await asyncio.to_thread(execute_query, OTPQueries.get_otp_by_user_id, (user_id,), conn=conn)
        return OTP(**row) if row else None

    async def get_verified_otp(self, user_id: int, code: str, conn=None) -> Optional[OTP]:
        row = await asyncio.to_thread(
            execute_query,
            OTPQueries.get_otp_by_code,
            (code, user_id),
            conn=conn
        )
        return OTP(**row) if row else None

    async def mark_otp_as_used(self, otp_id: int, conn=None) -> OTP:
        row = await asyncio.to_thread(
            execute_query,
            OTPQueries.mark_otp_as_used,
            (otp_id,),
            conn=conn
        )
        return OTP(**row)

    async def delete_expired_otps(self, conn=None) -> int:
        return await asyncio.to_thread(execute_query, OTPQueries.delete_expired_otps, (), conn=conn)

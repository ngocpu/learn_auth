from datetime import datetime
from typing import Optional
from app.models.user import Token
from app.database import execute_query, TokenQueries
import asyncio

class TokenRepositories:
    async def save_token(self, user_id: int, token: str, expires_at: datetime, created_at: datetime, conn=None) -> Token:
        row = await asyncio.to_thread(
            execute_query,
            TokenQueries.save_token,
            (user_id, token, expires_at, created_at),
            conn=conn
        )
        return Token(**row)

    async def get_token_by_value(self, token: str, conn=None) -> Optional[Token]:
        row = await asyncio.to_thread(execute_query, TokenQueries.get_token_by_value, (token,), conn=conn)
        return Token(**row) if row else None

    async def deactivate_token(self, token_id: int, conn=None) -> Token:
        row = await asyncio.to_thread(execute_query, TokenQueries.deactivate_token, (token_id,), conn=conn)
        return Token(**row)

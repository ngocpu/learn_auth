from datetime import datetime
from typing import Optional
from app.models.user import Token
from app.database import execute_query, TokenQueries

class TokenRepositories:
    def save_token(self, user_id: int, token: str, expires_at: datetime, created_at: datetime) -> Token:
        row = execute_query(TokenQueries.save_token, (user_id, token, expires_at, created_at))
        return Token(**row)

    def get_token_by_value(self, token: str) -> Optional[Token]:
        row = execute_query(TokenQueries.get_token_by_value, (token,))
        return Token(**row) if row else None

    def deactivate_token(self, token_id: int) -> Token:
        row = execute_query(TokenQueries.deactivate_token, (token_id,))
        return Token(**row)

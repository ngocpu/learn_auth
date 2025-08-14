from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    provider_id: Optional[str] = None
    provider: str
    avatar: Optional[str] = None
    activate: bool

class OTP(BaseModel):
    id: int
    user_id: int
    code: str
    expires_at: datetime
    is_used: bool

class Token(BaseModel):
    id: int
    user_id: int
    token: str
    expires_at: datetime
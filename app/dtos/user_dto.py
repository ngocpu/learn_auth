# User DTOs (Pydantic models)
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    activate: bool = False

class UserSignup(UserBase):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=6)

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_data: UserBase

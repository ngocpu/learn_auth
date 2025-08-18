from pydantic import BaseModel, EmailStr
from typing import Optional

class UserInfo(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    activate: bool = False
    
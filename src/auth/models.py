from pydantic import BaseModel, EmailStr, Field
from users.models import UserInfo

class RegisterRequest(BaseModel):
    username:str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    
class ActivateRequest(BaseModel):
    email: EmailStr
    otp_code: str
    
class OauthRequest(BaseModel):
    code: str
    
class AuthResponse(BaseModel):
    access_token: str
    user_data: UserInfo
from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories import UserRepository, TokenRepositories,OTPRepositories
from app.services.mail_service import MailServices
from app.dtos.user_dto import UserSignup, UserLogin, AuthResponse
from app.services.auth_service import AuthService
router = APIRouter()

# Dependency to get AuthService instance
def get_auth_service():
    user_repo = UserRepository()
    otp_repo = OTPRepositories()
    token_repo = TokenRepositories()
    mail_service = MailServices()
    return AuthService(user_repo, otp_repo, token_repo, mail_service)

@router.post("/signup", response_model=None, status_code=status.HTTP_201_CREATED)
async def signup(user_req: UserSignup, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.sign_up(user_req)

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(user_req: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(user_req)

@router.post("/activate/{user_id}", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def activate_user(user_id: str, otp_code:str, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.activate_user(user_id, otp_code)

# @router.post("/oauth-login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
# async def oauth_login(user_req: dict, auth_service: AuthService = Depends(get_auth_service)):
#     return await auth_service.oauth_login(user_req)

# @router.post("/logout/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def logout(user_id: str, auth_service: AuthService = Depends(get_auth_service)):
#     await auth_service.logout(user_id)
#     return {"message": "User logged out successfully"}

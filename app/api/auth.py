from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.user_repository import UserRepository
from app.dtos.user_dto import UserSignup, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()

# Dependency to get AuthService instance
def get_auth_service():
    user_repo = UserRepository()
    return AuthService(user_repo)

@router.post("/signup", response_model=UserResponse)
def signup(user_req: UserSignup, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.sign_up(user_req)

@router.post("/login", response_model=UserResponse)
def login(user_req: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(user_req)

@router.post("/activate/{user_id}")
def activate_user(user_id: str, auth_service: AuthService = Depends(get_auth_service)):
    auth_service.activate_user(user_id)
    return {"message": "User activated successfully"}

@router.post("/oauth-login", response_model=UserResponse)
def oauth_login(user_req: dict, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.oauth_login(user_req)

@router.post("/logout/{user_id}")
def logout(user_id: str, auth_service: AuthService = Depends(get_auth_service)):
    auth_service.logout(user_id)
    return {"message": "User logged out successfully"}

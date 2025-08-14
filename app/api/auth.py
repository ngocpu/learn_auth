from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories import UserRepository, TokenRepositories, OTPRepositories
from app.services.mail_service import MailServices
from app.services.oauth import BaseOAuthService, GoogleOAuthService, FacebookOAuthService
from app.dtos.user_dto import UserSignup, UserLogin, AuthResponse, OTPRequest, OauthRequest
from app.services.auth_service import AuthService

router = APIRouter()

# Local auth dependencies
def get_auth_service_normal() -> AuthService:
    user_repo = UserRepository()
    otp_repo = OTPRepositories()
    token_repo = TokenRepositories()
    mail_service = MailServices()
    return AuthService(user_repo, otp_repo, token_repo, mail_service)

# Factory for getting OAuthService by provider
def get_oauth_service(provider: str) -> BaseOAuthService:
    if provider == "google":
        return GoogleOAuthService()
    elif provider == "facebook":
        return FacebookOAuthService()
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

# Dependency for AuthService with OAuth 
def get_auth_service_with_oauth(provider: str) -> AuthService:
    oauth_service = get_oauth_service(provider)
    user_repo = UserRepository()
    otp_repo = OTPRepositories()
    token_repo = TokenRepositories()
    mail_service = MailServices()
    return AuthService(user_repo, otp_repo, token_repo, mail_service, oauth_service=oauth_service)


# ===== Routes =====
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_req: UserSignup, auth_service: AuthService = Depends(get_auth_service_normal)):
    return await auth_service.sign_up(user_req)


@router.post("/login", response_model=AuthResponse)
async def login(user_req: UserLogin, auth_service: AuthService = Depends(get_auth_service_normal)):
    return await auth_service.login(user_req)


@router.post("/activate/{user_id}", response_model=AuthResponse)
async def activate_user(user_id: str, otp: OTPRequest, auth_service: AuthService = Depends(get_auth_service_normal)):
    return await auth_service.activate_user(user_id, otp_code=otp.otp_code)


@router.post("/{provider}", response_model=AuthResponse)
async def oauth_login(provider: str, oauth_request: OauthRequest):
    auth_service = get_auth_service_with_oauth(provider)
    return await auth_service.oauth_login(oauth_request.code, provider=provider)

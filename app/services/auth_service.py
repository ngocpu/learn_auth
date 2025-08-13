from dataclasses import dataclass
from app.repositories import UserRepository, OTPRepositories, TokenRepositories
from datetime import datetime, timedelta
from app.dtos.user_dto import UserSignup, UserLogin, AuthResponse
from app.services.mail_service import MailServices
from app.core import AppBaseError, UserAlreadyExistsError, OtpNotFoundOrInvalidError, UserNotFoundError, InvalidCredentialsError
from app.utils import hash_password, verify_password, generate_otp_code, create_access_token, create_refresh_token
import hashlib
@dataclass
class AuthService:
    user_repo: UserRepository
    otp_repo: OTPRepositories
    token_repo: TokenRepositories
    mail_service: MailServices

    async def sign_up(self, user_req:UserSignup) -> None:
        if self.user_repo.get_user_by_email(user_req.email):
            raise UserAlreadyExistsError("User with this email already exists")
        
        try:
            user = self.user_repo.create_user(
                email=user_req.email,
                password= hash_password(user_req.password),
                username=user_req.username,
                provider_id=None,
                provider="local",
                avatar=None
            )
        except Exception as e:
            raise AppBaseError(f"Internal server error: {str(e)}")
        
        otp_expiration = datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        otp_code = generate_otp_code()
        await self.otp_repo.save_otp_code(
            code=otp_code,
            user_id=user.id,
            expires_at=otp_expiration
        )
        
        self.mail_service.send_email(
            to=user_req.email,
            subject="Wellcome to Our Service",
            body=f"Your OTP code is {otp_code} (expires in {otp_expiration}) minutes."
        )
        
        return {
            "message": "User created successfully. Please check your email for the OTP code."
        }

    async def activate_user(self, user_id: str, otp_code: str) -> AuthResponse:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        otp_record = await self.otp_repo.get_verified_otp(
            code=otp_code,
            user_id=user_id
        )

        if not otp_record:
            raise OtpNotFoundOrInvalidError("Invalid or expired OTP")

        user.is_active = True
        await self.user_repo.update_user(user)
        await self.otp_repo.mark_otp_as_used(otp_record.id)

        payload = {
            "sub": str(user.id),
            "email": user.email,
        }
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        hash_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        await self.token_repo.save_token(user.id, hash_refresh_token, datetime.now() + timedelta(days=30), datetime.now())

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_data=user
        )

    async def login(self, user_req: UserLogin) -> AuthResponse:
        user = await self.user_repo.get_user_by_email(user_req.email)
        if not user or not user.verify_password(user_req.password):
            raise InvalidCredentialsError("Invalid email or password")
        
        payload = {
            "sub": str(user.id),
            "email": user.email,
        }
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        hash_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        await self.token_repo.save_token(user.id, hash_refresh_token, datetime.now() + timedelta(days=30), datetime.now())

        return AuthResponse(
            access_token= access_token,
            refresh_token= refresh_token,
            user_data= user
        )

    async def oauth_login(self, user_req:any) -> AuthResponse:
        """
        Handle OAuth login.
        This method should handle the logic for logging in a user via an OAuth provider.
        It should validate the OAuth token, retrieve user information, and return a AuthResponse.
        """
        pass

    async def logout(self, user_id: str) -> None:
        """
        Handle user logout.
        This method should handle the logic for logging out a user, such as revoking tokens.
        """
        pass
    
    async def refresh_token(self, user_id: str, refresh_token: str) -> AuthResponse:
        """
        Handle token refresh.
        This method should validate the refresh token and issue a new access token.
        """
        pass
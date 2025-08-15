from fastapi import Response 
from dataclasses import dataclass
from app.models import user
from app.repositories import UserRepository, OTPRepositories, TokenRepositories
from datetime import datetime, timedelta
from app.dtos.user_dto import UserSignup, UserLogin, AuthResponse, UserBase, ActivateRequest
from app.services.mail_service import MailServices
from app.services.oauth import BaseOAuthService
from app.database import get_db_connection
from app.core import AppBaseError, UserAlreadyExistsError, OtpNotFoundOrInvalidError, UserNotFoundError, InvalidCredentialsError
from app.utils import hash_password, verify_password, generate_otp_code, create_access_token, create_refresh_token
import hashlib
@dataclass
class AuthService:
    user_repo: UserRepository
    otp_repo: OTPRepositories
    token_repo: TokenRepositories
    mail_service: MailServices
    oauth_service: BaseOAuthService=None

    async def sign_up(self, user_req: UserSignup) -> dict:
        conn = get_db_connection()
        existing_user = await self.user_repo.get_user_by_email(user_req.email, conn=conn)
        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

        try:
            user = await self.user_repo.create_user(
                email=user_req.email,
                password=hash_password(user_req.password),
                username=user_req.username,
                provider_id=None,
                provider="local",
                avatar=None,
                conn=conn
            )
            
            print("user_data", user)
            otp_expiration = datetime.utcnow() + timedelta(minutes=30)
            otp_code = generate_otp_code()
            await self.otp_repo.save_otp_code(
                code=otp_code,
                user_id=user.id,
                expires_at=otp_expiration,
                conn=conn
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")

        finally:
            conn.close()
        subject = "Welcome to Our Service"
        body = f"Your OTP code is {otp_code} (expires at {otp_expiration.isoformat()} UTC)."
        await self.mail_service.send_email(user_req.email, subject, body)

        return {"email": user.email, "message": "User created successfully. Please check your email for the OTP code."}

    async def activate_user(self, activate_req: ActivateRequest, response: Response) -> AuthResponse:
        conn = get_db_connection()
        try:
            user = await self.user_repo.get_user_by_email(email=activate_req.email, conn=conn)
            if not user:
                raise UserNotFoundError("User not found")
            
            otp_record = await self.otp_repo.get_verified_otp(
                code=activate_req.otp_code,
                user_id=int(user.id),
                conn=conn
            )

            if not otp_record:
                raise OtpNotFoundOrInvalidError("Invalid or expired OTP")

            user.activate = True
            await self.user_repo.update_user(
                user_id=user.id,
                username=user.username,
                email=user.email,
                password=user.password,
                provider_id=user.provider_id,
                provider=user.provider,
                avatar=user.avatar,
                activate=user.activate,
                conn=conn
            )
            await self.otp_repo.mark_otp_as_used(otp_record.id, conn=conn)

            payload = {
                "sub": str(user.id),
                "email": user.email,
            }
            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)
            hash_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
            await self.token_repo.save_token(user.id, hash_refresh_token, datetime.now() + timedelta(days=30), datetime.now(), conn=conn)
            conn.commit()
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=datetime.now() + timedelta(days=30)
            )   
            return AuthResponse(
                access_token=access_token,
                user_data=UserBase.from_orm(user)
            )
        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")
        finally:
            conn.close()

    async def login(self, user_req: UserLogin, response: Response) -> AuthResponse:
        conn = get_db_connection()
        try:

            user = await self.user_repo.get_user_by_email(user_req.email, conn=conn)
            if not user or not verify_password(user_req.password, user.password):
                raise InvalidCredentialsError("Invalid email or password")
            
            payload = {
                "sub": str(user.id),
                "email": user.email,
            }
            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)
            hash_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
            await self.token_repo.save_token(user.id, hash_refresh_token, datetime.now() + timedelta(days=30), datetime.now(), conn=conn)
            conn.commit()
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=datetime.now() + timedelta(days=30)
            )
            return AuthResponse(
                access_token=access_token,
                user_data=UserBase.from_orm(user)
            )
        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")
        finally:
            conn.close()

    async def oauth_login(self, code: str, provider: str, response: Response) -> AuthResponse:
        conn = get_db_connection()
        try:
            provider_token = await self.oauth_service.get_token_from_code(code)
            user_info = await self.oauth_service.get_user_info(provider_token["access_token"])
            print("Google User Info:", user_info)

            existed_user = await self.user_repo.get_user_by_email(email=user_info.get("email"), conn=conn)

            if existed_user:
                if not existed_user.provider_id:
                    existed_user = await self.user_repo.update_user(
                        username=user_info.get("name"),
                        email=existed_user.email,
                        password=existed_user.password,
                        provider_id=user_info.get("id"),
                        provider=provider,
                        avatar=user_info.get("picture") or user_info.get("avatar"),
                        conn=conn
                    )
            else:
                existed_user = await self.user_repo.create_user(
                    username=user_info.get("name"),
                    email=user_info.get("email"),
                    password=None,
                    provider_id=user_info.get("id"),
                    provider=provider,
                    avatar=user_info.get("picture") or user_info.get("avatar"),
                    activate=True,
                    conn=conn
                )

            payload = {
                "sub": str(existed_user.id),
                "email": existed_user.email,
            }
            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)
            hash_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()

            await self.token_repo.save_token(
                existed_user.id,
                hash_refresh_token,
                datetime.now() + timedelta(days=30),
                datetime.now(),
                conn=conn
            )

            conn.commit()
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=datetime.now() + timedelta(days=30)
            )
            return AuthResponse(
                access_token=access_token,
                user_data=UserBase.from_orm(existed_user)
            )

        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")

        finally:
            conn.close()

    async def logout(self, token:str, response: Response) -> None:
        if not token:
            raise AppBaseError("No refresh token provided")
        conn = get_db_connection()
        try:
            hash_token = hashlib.sha256(token.encode()).hexdigest()
            await self.token_repo.revoke_token(hash_token, conn=conn)
            response.delete_cookie(
                key="refresh_token",
                path="/",
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")
        finally:
            conn.close()
    
    async def refresh_token(self, refresh_token: str, response:Response) -> AuthResponse:
        if not refresh_token:
            raise AppBaseError("No refresh token provided")
        conn = get_db_connection()
        try:
            hash_token = hashlib.sha256(refresh_token.encode()).hexdigest()
            valid_token = await self.token_repo.get_valid_token(hash_token, conn=conn)
            print("valid_token", valid_token)
            if not valid_token:
                raise AppBaseError("Invalid or expired refresh token")

            user = await self.user_repo.get_user_by_id(valid_token["user_id"], conn=conn)

            # if token valid, create new token and sent back to client
            new_access_token = create_access_token({"sub": user.id, "email": user.email})
            new_refresh_token = create_refresh_token({"sub": user.id, "email": user.email})
            refresh_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
            await self.token_repo.save_token(
                user_id=int(user.id),
                token=refresh_token_hash,
                expires_at=datetime.now() + timedelta(days=30),
                created_at=datetime.now(),
                conn=conn
            )
            conn.commit()
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=datetime.now() + timedelta(days=30)
            )
            return AuthResponse(
                access_token=new_access_token,
                user_data=UserBase.from_orm(user)
            )
        except Exception as e:
            conn.rollback()
            raise AppBaseError(f"Internal server error: {str(e)}")
        finally:
            conn.close()

import logging
from entities.token import RefreshToken
from .repositories.auth_refresh_token_repo import TokenRepositories
from src.exception import GlobalError

class TokenService:
    def __init__(self, token_repo: TokenRepositories):
        self.token_repo = token_repo

    def get_valid_token(self, user_id, token) -> RefreshToken:
        valid_token = self.token_repo.get_valid_token(user_id, token)
        if not valid_token:
            logging.error(f"Valid refresh token not found for user_id: {user_id}")
            raise GlobalError("Invalid or expired refresh token")
        logging.info(f"Valid refresh token found for user_id: {user_id}")
        return valid_token

    def save_token(self, user_id, token, expires_at) -> RefreshToken:
        try:
            saved_token = self.token_repo.save_token(user_id, token, expires_at)
            logging.info(f"Refresh token saved for user_id: {user_id}")
            return saved_token
        except Exception as e:
            logging.error(f"Failed to save refresh token for user_id: {user_id}: {str(e)}")
            raise GlobalError("Failed to save refresh token")

    def revoke_token(self, user_id, token) -> bool:
        try:
            result = self.token_repo.revoke_token(user_id, token)
            if result:
                logging.info(f"Refresh token revoked for user_id: {user_id}")
                return True
            else:
                logging.warning(f"No valid refresh token found to revoke for user_id: {user_id}")
                return False
        except Exception as e:
            logging.error(f"Failed to revoke refresh token for user_id: {user_id}: {str(e)}")
            raise GlobalError("Failed to revoke refresh token")
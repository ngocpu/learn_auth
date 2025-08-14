# plan to make other oauth method....
from .base_oauth_service import BaseOAuthService
class FacebookOAuthService(BaseOAuthService):
    async def get_user_info(self, access_token: str) -> dict:
        # Implement logic to get user info from Facebook API
        pass
    async def get_token_from_code(self, code: str) -> dict:
        # Implement logic to exchange code for access token
        pass
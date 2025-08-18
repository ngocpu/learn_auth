from .base import BaseOAuthService
from src.setting import settings
from src.exception import GlobalError
import aiohttp

class GoogleOAuthService(BaseOAuthService):
    async def get_token_from_code(self, code):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.GG_TOKEN_URL,
                data={
                    'code': code,
                    'client_id': settings.GG_CLIENT_ID,
                    'client_secret': settings.GG_SECRET,
                    'redirect_uri': settings.GG_REDIRECT_URI,
                    'grant_type': 'authorization_code'
                }
            ) as response:
                if response.status != 200:
                    raise GlobalError(f"Failed to exchange code: {await response.text()}")
                return await response.json()
    
    async def get_user_info(self, access_token):
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.GG_USER_INFO_URL, headers={
                'Authorization': f'Bearer {access_token}'
            }) as response:
                if response.status != 200:
                    raise GlobalError(f"Failed to get user info: {await response.text()}")
                return await response.json()
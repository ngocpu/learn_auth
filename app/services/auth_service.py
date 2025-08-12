from app.repositories.user_repository import UserRepository
from app.dtos.user_dto import UserSignup, UserLogin, UserResponse
class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def sign_up(self, user_req: UserSignup) -> UserResponse:
        # Implement sign-up logic
        pass

    def activate_user(self, user_id: str) -> None:
        # Implement user activation logic
        pass

    def login(self, user_req: UserLogin) -> UserResponse:
        # Implement login logic
        pass
    
    def oauth_login(self, user_req:any) -> UserResponse:
        """
        Handle OAuth login.
        This method should handle the logic for logging in a user via an OAuth provider.
        It should validate the OAuth token, retrieve user information, and return a UserResponse.
        """
        pass

    def logout(self, user_id: str) -> None:
        """
        Handle user logout.
        This method should handle the logic for logging out a user, such as revoking tokens.
        """
        pass
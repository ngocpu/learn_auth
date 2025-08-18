from abc import ABC, abstractmethod
class BaseOAuthService(ABC):
    @abstractmethod
    def get_token_from_code(self, code: str) -> dict:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> dict:
        pass

from .oauth.base import BaseOAuthService
from src.users.user_service import UserServices
from src.mails.mail_services import MailServices
from src.exception import GlobalError

class AuthServices:
    def __init__(self, oauth: BaseOAuthService, user_service: UserServices, mail_service: MailServices):
        self.oauth = oauth
        self.user_service = user_service
        self.mail_service = mail_service
        self.user_service = user_service
        
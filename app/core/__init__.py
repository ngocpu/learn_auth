# Place for core settings, config, and security utils
from .global_setting import settings
from .exception import AppBaseError, UserAlreadyExistsError, OtpNotFoundOrInvalidError, InvalidCredentialsError, PermissionDeniedError, UserNotFoundError, app_exception_handler, unhandled_exception_handler
__all__ = [
    "settings",
    "AppBaseError",
    "UserAlreadyExistsError",
    "OtpNotFoundOrInvalidError",
    "InvalidCredentialsError",
    "PermissionDeniedError",
    "UserNotFoundError",
    "app_exception_handler",
    "unhandled_exception_handler"
]

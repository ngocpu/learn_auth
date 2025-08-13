from fastapi import status, Request
from fastapi.responses import JSONResponse
class AppBaseError(Exception):
    pass

class UserAlreadyExistsError(AppBaseError):
    pass

class UserNotFoundError(AppBaseError):
    pass

class OtpNotFoundOrInvalidError(AppBaseError):
    pass

class InvalidCredentialsError(AppBaseError):
    pass

class PermissionDeniedError(AppBaseError):
    pass

ERROR_MAPPING = {
    UserAlreadyExistsError: (status.HTTP_409_CONFLICT, "USER_ALREADY_EXISTS"),
    UserNotFoundError: (status.HTTP_404_NOT_FOUND, "USER_NOT_FOUND"),
    OtpNotFoundOrInvalidError: (status.HTTP_400_BAD_REQUEST, "INVALID_OTP"),
    InvalidCredentialsError: (status.HTTP_401_UNAUTHORIZED, "INVALID_CREDENTIALS"),
    PermissionDeniedError: (status.HTTP_403_FORBIDDEN, "PERMISSION_DENIED"),
}
# excetion handler
async def app_exception_handler(request: Request, exc: AppBaseError):
    status_code, error_code = ERROR_MAPPING.get(type(exc), (status.HTTP_400_BAD_REQUEST, "BAD_REQUEST"))
    
    return JSONResponse(
        status_code=status_code,
        content={
            "message": str(exc) or error_code.replace("_", " ").title(),
            "error_code": error_code
        }
        
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error", "error_code": "SERVER_ERROR"}
    )
from fastapi import HTTPException

class GlobalError(HTTPException):
    pass

class UserError(HTTPException):
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)
        
class UserAlreadyExistsError(UserError):
    def __init__(self, email=None):
        message = "User already exists" if email is None else f"User with email {email} already exists"
        super().__init__(status_code=409, detail=message)
        
class InvalidCredentialsError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid password")
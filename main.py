from fastapi import FastAPI
from app.api import auth
from app.core.exception import AppBaseError, app_exception_handler, unhandled_exception_handler
app = FastAPI()
app.add_exception_handler(AppBaseError, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include your auth router
app.include_router(auth.router, prefix="/auth")
@app.get("/")
def root():
    return {"message": "Welcome to the Auth API"}

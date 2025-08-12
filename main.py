from fastapi import FastAPI
from app.api import auth
app = FastAPI()

# Include your auth router
app.include_router(auth.router, prefix="/auth")
@app.get("/")
def root():
    return {"message": "Welcome to the Auth API"}

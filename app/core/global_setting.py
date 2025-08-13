
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI Auth Project"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("JWT_SECRET", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DB_NAME: str = os.getenv("DB_NAME", "your_db")
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    EMAIL_SMTP_SERVER: str = os.getenv("MAIL_SMTP_SERVER", "smtp.example.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("MAIL_SMTP_PORT", 587))
    EMAIL_SMTP_USER: str = os.getenv("MAIL_USERNAME", "user")
    EMAIL_SMTP_PASSWORD: str = os.getenv("MAIL_PASSWORD", "password")
    GG_CLIENT_ID: str = os.getenv("GG_CLIENT_ID", "")
    GG_SECRET: str = os.getenv("GG_SECRET", "")

settings = Settings()

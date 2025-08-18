from src.database.core import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(155), unique=False, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    provider_id = Column(String(255), nullable=True)
    provider = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    activate = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(email='{self.email}', username='{self.username}', created_at='{self.created_at}')>"

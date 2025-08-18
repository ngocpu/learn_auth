from database.core import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<RefreshToken(user_id='{self.user_id}', token='{self.token}', expires_at='{self.expires_at}')>"
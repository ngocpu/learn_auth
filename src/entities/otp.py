from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from database.core import Base
from datetime import datetime

class Otp(Base):
    __tablename__ = "otp_code"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    code = Column(String(6), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    
    def __repr__(self):
        return f"<Otp(user_id='{self.user_id}', code='{self.code}', created_at='{self.created_at}', is_used='{self.is_used}', expires_at='{self.expires_at}')>"


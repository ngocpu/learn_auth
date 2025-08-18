from sqlalchemy.orm import Session
from src.entities.otp import Otp as OTP
from datetime import datetime

class OtpRepositories:
    def __init__(self, db: Session):
        self.db = db
    
    def get_otp_by_user_id(self, user_id:int) -> OTP:
        return self.db.query(OTP).filter(OTP.user_id == user_id).first()
    
    def get_valid_otp(self, otp:str, user_id:int) -> OTP:
        return self.db.query(OTP).filter(OTP.code == otp, OTP.user_id == user_id, OTP.is_used == False, OTP.expires_at > datetime.now()).first()
    
    def save_otp(self, otp:str, user_id:int) ->OTP:
        self.db.add(
            OTP(
                user_id=user_id,
                code=otp,
                expires_at=datetime.now(),
                is_used=False
            )
        )
        self.db.commit()
        self.db.refresh(otp)
        return OTP(
            user_id=user_id,
            code=otp,
            expires_at=datetime.now(),
            is_used=False
        )
        
    def mark_otp_as_used(self, otp: OTP) -> OTP:
        return self.update_otp(otp, is_used=True)
        
    
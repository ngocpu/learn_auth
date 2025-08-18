from sqlalchemy.orm import Session
from datetime import datetime
from entities.token import RefreshToken

class TokenRepositories:
    def __init__(self, db: Session):
        self.db = db
    
    def get_valid_token(self, user_id, token):
        return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id, RefreshToken.token == token, RefreshToken.expires_at > datetime.now()).first()
    
    def save_token(self, user_id, token, expires_at):
        self.db.add(
            RefreshToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at
            )
        )
        self.db.commit()
        self.db.refresh(token)
        return RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=datetime.now(),
        )
        
    def revoke_token(self, user_id, token):
        refresh_token = self.get_valid_token(user_id, token)
        if refresh_token:
            self.db.delete(refresh_token)
            self.db.commit()
            return True
        return False
    
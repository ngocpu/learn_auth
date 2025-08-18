from sqlalchemy.orm import Session
from src.entities.users import User
from .models import UserInfo
from src.database import execute_query, UserQueries
import asyncio


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ORM methods
    def get_user_by_id(self, user_id: int) -> UserInfo:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> UserInfo:
        return self.db.query(UserInfo).filter(UserInfo.email == email).first()

    def get_user_by_username(self, username: str) -> UserInfo:
        return self.db.query(UserInfo).filter(UserInfo.username == username).first()

    def get_user_by_provider_id(self, provider_id: str, provider: str) -> UserInfo:
        return (
            self.db.query(UserInfo)
            .filter(UserInfo.provider_id == provider_id, UserInfo.provider == provider)
            .first()
        )

    def create_user(self, user: UserInfo) -> UserInfo:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: UserInfo, **kwargs) -> UserInfo:
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: UserInfo):
        self.db.delete(user)
        self.db.commit()

    def activate_user(self, user: UserInfo) -> UserInfo:
        user.activate = True
        self.db.commit()
        self.db.refresh(user)
        return user


    async def get_all_users(self, conn=None) -> list[User]:
        rows = await asyncio.to_thread(
            execute_query, UserQueries.get_all_users, None, False, conn=conn
        )
        return [User(**row) for row in rows]

from app.models.user import User  # import model ở bước 1
from app.database import execute_query, UserQueries
import asyncio

class UserRepository:
    async def get_user_by_id(self, user_id, conn=None) -> User:
        row = await asyncio.to_thread(execute_query, UserQueries.get_user_by_id, (user_id,), conn=conn)
        return User(**row) if row else None

    async def get_user_by_username(self, username, conn=None) -> User:
        row = await asyncio.to_thread(execute_query, UserQueries.get_user_by_username, (username,), conn=conn)
        return User(**row) if row else None

    async def get_user_by_email(self, email, conn=None) -> User:
        row = await asyncio.to_thread(execute_query, UserQueries.get_user_by_email, (email,), conn=conn)
        return User(**row) if row else None

    async def get_user_by_provider_id(self, provider_id, provider, conn=None) -> User:
        row = await asyncio.to_thread(execute_query, UserQueries.get_user_by_provider_id, (provider_id, provider), conn=conn)
        return User(**row) if row else None

    async def get_all_users(self, conn=None) -> list[User]:
        rows = await asyncio.to_thread(execute_query, UserQueries.get_all_users, None, False, conn=conn)
        return [User(**row) for row in rows]

    async def create_user(self, username, email, password, provider_id, provider, avatar, activate=False, conn=None) -> User:
        row = await asyncio.to_thread(
            execute_query,
            UserQueries.create_user,
            (username, email, password, provider_id, provider, avatar, activate),
            conn=conn
        )
        return User(**row)

    async def update_user(self, user_id, username, email, password, provider_id, provider, avatar, activate, conn=None) -> User:
        row = await asyncio.to_thread(
            execute_query,
            UserQueries.update_user,
            (username, email, password, provider_id, provider, avatar, activate, user_id),
            conn=conn
        )
        return User(**row)

    async def delete_user(self, user_id, conn=None):
        return await asyncio.to_thread(execute_query, UserQueries.delete_user, (user_id,), conn=conn)

    async def activate_user(self, user_id, conn=None) -> User:
        row = await asyncio.to_thread(execute_query, UserQueries.activate_user, (user_id,), conn=conn)
        return User(**row)

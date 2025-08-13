from app.models.user import User  # import model ở bước 1
from app.database import execute_query, UserQueries
class UserRepository:
    def get_user_by_id(self, user_id) -> User:
        row = execute_query(UserQueries.get_user_by_id, (user_id,))
        return User(**row) if row else None

    def get_user_by_username(self, username) -> User:
        row = execute_query(UserQueries.get_user_by_username, (username,))
        return User(**row) if row else None

    def get_user_by_email(self, email) -> User:
        row = execute_query(UserQueries.get_user_by_email, (email,))
        return User(**row) if row else None

    def get_user_by_provider_id(self, provider_id, provider) -> User:
        row = execute_query(UserQueries.get_user_by_provider_id, (provider_id, provider))
        return User(**row) if row else None

    def get_all_users(self) -> list[User]:
        rows = execute_query(UserQueries.get_all_users)
        return [User(**row) for row in rows]

    def create_user(self, username, email, password, provider_id, provider, avatar, activate=False) -> User:
        row = execute_query(
            UserQueries.create_user,
            (username, email, password, provider_id, provider, avatar, activate)
        )
        return User(**row)

    def update_user(self, user_id, username, email, password, provider_id, provider, avatar, activate) -> User:
        row = execute_query(
            UserQueries.update_user,
            (username, email, password, provider_id, provider, avatar, activate, user_id)
        )
        return User(**row)

    def delete_user(self, user_id):
        return execute_query(UserQueries.delete_user, (user_id,))

    def activate_user(self, user_id) -> User:
        row = execute_query(UserQueries.activate_user, (user_id,))
        return User(**row)

# User repository for database operations
from app.database.queries.user import UserQueries
from app.database import execute_query

class UserRepository:
    def get_user_by_id(self, user_id):
        return execute_query(UserQueries.get_user_by_id, (user_id,))

    def get_user_by_username(self, username):
        return execute_query(UserQueries.get_user_by_username, (username,))

    def get_user_by_email(self, email):
        return execute_query(UserQueries.get_user_by_email, (email,))

    def get_user_by_provider_id(self, provider_id, provider):
        return execute_query(UserQueries.get_user_by_provider_id, (provider_id, provider))

    def get_all_users(self):
        return execute_query(UserQueries.get_all_users)

    def create_user(self, username, email, password, provider_id, provider, avatar, activate=False):
        return execute_query(
            UserQueries.create_user,
            (username, email, password, provider_id, provider, avatar, activate)
        )

    def update_user(self, user_id, username, email, password, provider_id, provider, avatar, activate):
        return execute_query(
            UserQueries.update_user,
            (username, email, password, provider_id, provider, avatar, activate, user_id)
        )

    def delete_user(self, user_id):
        return execute_query(UserQueries.delete_user, (user_id,))

    def activate_user(self, user_id):
        return execute_query(UserQueries.activate_user, (user_id,))

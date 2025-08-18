from . import models
from .user_repositories import UserRepository
from src.entities.users import User
from src.exception import UserNotFoundError, InvalidPasswordError, UserAlreadyExistsError
import logging

class UserServices:
    def __init__(self, repo:UserRepository):
        self.repo = repo
    
    def get_user_by_id(self, user_id: int) -> models.UserInfo:
        user = self.repo.get_user_by_id(user_id)
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise UserNotFoundError(user_id)
        logging.info(f"User with id {user_id} found")
        return user
    
    def get_user_by_email(self, email: str) -> models.UserInfo:
        user = self.repo.get_user_by_email(email)
        if user:
            logging.warning(f"User with email {email} already exists")
            raise UserAlreadyExistsError(email)
        
    def get_all_user(self) -> list[models.UserInfo]:
        users = self.repo.get_all_users()
        if not users:
            logging.info("No users found")
        else:
            logging.info(f"Found {len(users)} users")
        return users
    
    def create_user(self, user) -> models.UserInfo:
        existing_user = self.repo.get_user_by_email(user.email)
        if existing_user:
            logging.warning(f"User with email {user.email} already exists")
            raise UserAlreadyExistsError(user.email)
        
        new_user = self.repo.create_user(user)
        logging.info(f"User with id {new_user.id} created successfully")
        return new_user
    
    def update_user(self, user, **kwargs) -> models.UserInfo:
        updated_user = self.repo.update_user(user, **kwargs)
        logging.info(f"User with id {updated_user.id} updated successfully")
        return updated_user

    def delete_user(self, user):
        self.repo.delete_user(user)
        logging.info(f"User with id {user.id} deleted successfully")

    def activate_user(self, user) -> models.UserInfo:
        activated_user = self.repo.activate_user(user)
        logging.info(f"User with id {activated_user.id} activated successfully")
        return activated_user
        
        
from .repositories.auth_otp_repo import OtpRepositories
import logging
from src.exception import UserNotFoundError, GlobalError
from src.entities.otp import Otp as OTP

class OtpServices:
    def __init__(self, otp_repo: OtpRepositories):
        self.otp_repo = otp_repo

    def get_otp_by_user_id(self, user_id: int) -> OTP:
        otp_code = self.otp_repo.get_otp_by_user_id(user_id)
        if not otp_code:
            logging.error(f"OTP not found for user_id: {user_id}")
            raise UserNotFoundError(f"OTP not found for user_id: {user_id}")
        logging.info(f"OTP retrieved for user_id: {user_id}")
        return otp_code

    def get_valid_otp(self, otp: str, user_id: int) -> OTP:
        valid_otp = self.otp_repo.get_valid_otp(otp, user_id)
        if not valid_otp:
            logging.error(f"Valid OTP not found for user_id: {user_id} and code: {otp}")
            raise GlobalError("Invalid or expired OTP code")
        logging.info(f"Valid OTP found for user_id: {user_id}")
        return valid_otp

    def save_otp(self, otp: str, user_id: int) -> OTP:
        try:
            saved_otp = self.otp_repo.save_otp(otp, user_id)
            logging.info(f"OTP saved for user_id: {user_id}")
            return saved_otp
        except Exception as e:
            logging.error(f"Failed to save OTP for user_id: {user_id}: {str(e)}")
            raise GlobalError("Failed to save OTP code")

    def mark_otp_as_used(self, otp: OTP) -> OTP:
        try:
            used_otp = self.otp_repo.mark_otp_as_used(otp)
            logging.info(f"OTP marked as used for user_id: {otp.user_id}")
            return used_otp
        except Exception as e:
            logging.error(f"Failed to mark OTP as used for user_id: {otp.user_id}: {str(e)}")
            raise GlobalError("Failed to mark OTP as used")






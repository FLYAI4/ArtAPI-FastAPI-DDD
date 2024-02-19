from sqlalchemy.orm import Session
from src.account.domain.entity import UserInfo
from src.account.domain.exception import UserError
from src.account.domain.errorcode import LogInError
from src.account.domain.util.cipher import CipherManager
from src.account.infra.database.repository import AccountRepository


class LogInService:
    def log_in_user(self, session: Session, user_info: UserInfo):
        # Validate user's input data
        self.__check_user_id_existence(session, user_info.id)
        self.__check_user_password(session, user_info)

        # Validate password collect.

        # Generate token
        pass

    @staticmethod
    def __check_user_id_existence(session: Session, user_id: str):
        """Check user is registed."""
        all_user_account = AccountRepository.get_all_user_account(session)
        if not any(account.id == user_id for account in all_user_account):
            raise UserError(**LogInError.NonSignupError.value)

    @staticmethod
    def __check_user_password(session: Session, user_info: UserInfo):
        user_account = AccountRepository.get_user_account(session, user_info)
        original_password = CipherManager().decrypt_password(user_account.password)
        if user_info.password != original_password:
            raise UserError(**LogInError.WrongPasswordError.value)

import re
from sqlalchemy.orm import Session
from src.account.domain.entity import AccountInfo
from src.account.domain.exception import UserError
from src.account.domain.errorcode import SignUpError
from src.account.infra.database.repository import AccountRepository
from src.account.domain.util.cipher import CipherManager


class SignUpService:

    def sign_up_user(
            self, session: Session, user_account: AccountInfo
    ) -> AccountInfo:
        # Validate user's input data
        self.__check_user_id_pattern(user_account.id)
        self.__check_user_existence(session, user_account.id)

        # Encrypt password
        encrypt_password = CipherManager().encrypt_password(
            user_account.password
            )
        user_account.password = encrypt_password
        return user_account

    @staticmethod
    def __check_user_id_pattern(user_id: str):
        """Check ID is in email pattern."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, user_id):
            raise UserError(**SignUpError.NonMatchEmail.value)

    @staticmethod
    def __check_user_existence(session: Session, user_id: str):
        """Check user has already been created."""
        user_id_prefix = user_id.split("@")[0]
        all_user_account = AccountRepository.get_all_user_account(session)
        for account in all_user_account:
            account_prefix = account.id.split("@")[0]
            if user_id_prefix == account_prefix:
                raise UserError(**SignUpError.AlreadyUserError.value)

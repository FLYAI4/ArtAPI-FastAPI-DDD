from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.account.domain.entity import AccountInfo, UserInfo


class AccountRepositoryABS(ABC):
    @abstractmethod
    def insert_user_account(
        self, session: Session, user_account: AccountInfo
    ) -> UserInfo:
        pass

    @abstractmethod
    def get_user_account(
        self, session: Session, user_info: UserInfo
    ) -> AccountInfo:
        pass

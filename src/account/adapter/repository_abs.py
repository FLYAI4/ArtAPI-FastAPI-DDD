from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.account.domain.entity import AccountInfo, UserInfo


class AccountRepositoryABS(ABC):
    @abstractmethod
    def insert_user_account(
        self, session: Session, account: AccountInfo
    ) -> UserInfo:
        pass

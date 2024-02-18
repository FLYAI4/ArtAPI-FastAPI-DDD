from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.account.domain.entity import AccountInfo, UserInfo
from typing import List


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

    @abstractmethod
    def get_all_user_account(self, session: Session) -> List[UserInfo]:
        pass

    @abstractmethod
    def delete_user_account(
        self, session: Session, user_info: UserInfo
    ) -> UserInfo:
        pass

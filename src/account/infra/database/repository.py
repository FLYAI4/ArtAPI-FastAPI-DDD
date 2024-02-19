from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.account.adapter.database import AccountRepositoryInterface
from src.account.domain.entity import AccountInfo, UserInfo
from src.account.infra.database.model import Account
from src.shared_kernel.domain.exception import DBError
from src.account.domain.errorcode import RepositoryError


class AccountRepository(AccountRepositoryInterface):
    def insert_user_account(
            session: Session, user_account: AccountInfo
    ) -> UserInfo:
        try:
            obj = Account(
                id=user_account.id,
                password=user_account.password,
                name=user_account.name,
                gender=user_account.gender,
                age=user_account.age
            )
            with session:
                session.add(obj)
                session.commit()
            return UserInfo(id=user_account.id)
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def get_user_account(
            session: Session, user_info: UserInfo
    ) -> AccountInfo:
        try:
            with session:
                sql = select(Account).filter(Account.id == user_info.id)
                obj = session.execute(sql).scalar_one()
                return AccountInfo(
                    id=obj.id,
                    password=obj.password,
                    name=obj.name,
                    gender=obj.gender,
                    age=obj.age,
                    status=obj.status
                )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def get_all_user_account(session: Session) -> List[UserInfo]:
        try:
            all_user_account = list()
            with session:
                sql = select(Account)
                for obj in session.execute(sql):
                    all_user_account.append(UserInfo(id=obj.Account.id))
            return all_user_account
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def delete_user_account(
            session: Session, user_info: UserInfo
    ) -> UserInfo:
        try:
            with session:
                sql = select(Account).filter(Account.id == user_info.id)
                obj = session.execute(sql).scalar_one()
                if obj:
                    session.delete(obj)
                session.commit()
            return UserInfo(id=user_info.id)
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

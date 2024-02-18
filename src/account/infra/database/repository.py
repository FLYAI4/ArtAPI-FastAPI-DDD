from sqlalchemy.orm import Session
from src.account.adapter.repository_abs import AccountRepositoryABS
from src.account.domain.entity import AccountInfo, UserInfo
from src.account.infra.database.model import Account
from src.account.domain.exception import DBError
from src.account.domain.errorcode import RepositoryError


class AccountRepository(AccountRepositoryABS):
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

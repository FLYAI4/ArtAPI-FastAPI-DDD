from sqlalchemy.orm import Session
from src.account.adapter.rest.request import SignUpUserRequest
from src.account.domain.service.sign_up import SignUpService
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo, UserInfo


class AccountCommandUseCase:
    def __init__(
            self,
            sign_up_service: SignUpService,
            account_repository: AccountRepository,
            session: Session
    ) -> None:
        self.service = sign_up_service()
        self.repository = account_repository
        self.session = session

    def sign_up_user(self, request: SignUpUserRequest) -> UserInfo:
        # convert request -> entity
        user_account = AccountInfo(
            id=request.id,
            password=request.password,
            name=request.name,
            gender=request.gender,
            age=request.gender
        )

        # sign up
        user_account = self.service.sign_up_user(self.session, user_account)

        # save DB
        user_info = self.repository.insert_user_account(self.session, user_account)
        return user_info

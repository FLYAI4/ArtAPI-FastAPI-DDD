from sqlalchemy.orm import Session
from src.account.adapter.rest.request import SignUpUserRequest, LogInUserRequest
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.service.log_in import LogInService
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo, UserInfo, TokenInfo
from src.shared_kernel.domain.jwt import TokenManager


class AccountCommandUseCase:
    def __init__(
            self,
            account_repository: AccountRepository,
            session: Session
    ) -> None:
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

        # check sign up
        user_account = SignUpService().sign_up_user(self.session, user_account)

        # save DB
        user_info = self.repository.insert_user_account(self.session, user_account)
        return user_info

    def log_in_user(self, request: LogInUserRequest) -> UserInfo:
        # convert request -> entity
        user_info = UserInfo(
            id=request.id,
            password=request.password
        )

        # check log in 
        user_id = LogInService().log_in_user(self.session, user_info)

        # make token
        token = TokenManager().create_token(user_id)
        return TokenInfo(
            id=user_id,
            token=token
        )


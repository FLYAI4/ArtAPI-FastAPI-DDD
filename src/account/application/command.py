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
            account_repo: AccountRepository,
            signup_service: SignUpService,
            login_service: LogInService,
            postgre_session: Session
    ) -> None:
        self.account_repo = account_repo
        self.signup_service = signup_service
        self.login_service = login_service
        self.postgre_session = postgre_session

    def sign_up_user(self, request: SignUpUserRequest) -> UserInfo:
        # convert request -> entity
        user_account = AccountInfo(
            id=request.id,
            password=request.password,
            name=request.name,
            gender=request.gender,
            age=request.gender
        )
        try:
            # check sign up
            user_account = self.signup_service.sign_up_user(self.postgre_session, user_account)

            # save DB
            user_info = self.account_repo.insert_user_account(self.postgre_session, user_account)
            return user_info
        except Exception as e:
            print(e)

    def log_in_user(self, request: LogInUserRequest) -> TokenInfo:
        # convert request -> entity
        user_info = UserInfo(
            id=request.id,
            password=request.password
        )

        # check log in
        user_id = self.login_service.log_in_user(self.postgre_session, user_info)

        # make token
        token = TokenManager().create_token(user_id)
        return TokenInfo(
            id=user_id,
            token=token
        )

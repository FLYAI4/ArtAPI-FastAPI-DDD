from dependency_injector import containers, providers
from src.account.infra.database.repository import AccountRepository
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.service.log_in import LogInService
from src.account.application.command import AccountCommandUseCase
from src.shared_kernel.infra.database.connection import PostgreManager


class AccountContainer(containers.DeclarativeContainer):
    account_repo = providers.Factory(AccountRepository)
    singup_service = providers.Factory(SignUpService)
    login_service = providers.Factory(LogInService)

    account_command = providers.Factory(
        AccountCommandUseCase,
        account_repo=account_repo,
        signup_service=singup_service,
        login_service=login_service,
        postgre_session=PostgreManager.get_session
    )

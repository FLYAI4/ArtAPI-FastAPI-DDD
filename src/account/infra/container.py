from dependency_injector import containers, providers
from src.account.infra.database.repository import AccountRepository
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.service.log_in import LogInService

class AccountContainer(containers.DeclarativeContainer):
    account_repo = providers.Factory(AccountRepository)
    singup_service = providers.Factory(SignUpService)
    login_service = providers.Factory(LogInService)

    

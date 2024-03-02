from dependency_injector import containers, providers
from src.account.infra.container import AccountContainer
from src.admin.infra.container import AdminContainer
from src.user.infra.container import UserContainer


class AppContainer(containers.DeclarativeContainer):
    # wiring_config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.account.adapter.rest.api",
            "src.admin.adapter.rest.api",
            "src.user.adapter.rest.api"
        ]
    )
    account = providers.Container(AccountContainer)
    admin = providers.Container(AdminContainer)
    user = providers.Container(UserContainer)

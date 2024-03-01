from dependency_injector import containers, providers
from src.account.infra.container import AccountContainer


class AppContainer(containers.DeclarativeContainer):
    # wiring_config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.account.adapter.rest.api",
        ]
    )
    account = providers.Container(AccountContainer)

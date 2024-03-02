from dependency_injector import containers, providers
from src.user.infra.database.repository import UserRepository
from src.user.domain.service.insert_image import InsertImageService
from src.user.application.command import UserCommandUseCase
from src.shared_kernel.infra.database.connection import (
    MongoManager,
    PostgreManager,
    BlobStorageManager
)


class UserContainer(containers.DeclarativeContainer):
    user_repository = providers.Factory(UserRepository)
    insert_image_service = providers.Factory(InsertImageService)

    user_command = providers.Factory(
        UserCommandUseCase,
        user_repository=user_repository,
        insert_image_service=insert_image_service,
        mongo_session=MongoManager.get_session,
        postgre_session=PostgreManager.get_session,
        azure_blob_session=BlobStorageManager.get_session,
    )

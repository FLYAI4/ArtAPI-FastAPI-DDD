from dependency_injector import containers, providers
from src.admin.infra.database.repository import AdminRepository
from src.admin.domain.service.generated_content import GeneratedContentService
from src.admin.application.command import AdminCommandUseCase
from src.shared_kernel.infra.database.connection import MongoManager, BlobStorageManager


class AdminContainer(containers.DeclarativeContainer):
    admin_repo = providers.Factory(AdminRepository)
    generated_content_service = providers.Factory(GeneratedContentService)

    admin_command = providers.Factory(
        AdminCommandUseCase,
        admin_repo=admin_repo,
        generated_content_service=generated_content_service,
        mongo_session=MongoManager.get_session,
        azure_blob_session=BlobStorageManager.get_session
    )

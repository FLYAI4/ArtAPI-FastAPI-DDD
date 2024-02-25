from abc import ABC, abstractmethod
from src.admin.domain.entity import GeneratedContent, GeneratedContentName


class AdminRepositoryInterface(ABC):
    @abstractmethod
    def insert_content(
        azure_blob_session, generated_content: GeneratedContent
    ) -> GeneratedContentName:
        pass

    @abstractmethod
    def delete_content(
        azure_blob_session, generated_content_name: GeneratedContentName
    ) -> GeneratedContentName:
        pass

from abc import ABC, abstractmethod
from src.user.domain.entity import GeneratedContentModel, GeneratedIdInfo


class UserRepositoryInterface(ABC):
    @abstractmethod
    def insert_content(
        mongo_session, generated_content: GeneratedContentModel
    ) -> GeneratedIdInfo:
        pass

    @abstractmethod
    def insert_generated_id(
        postgre_session, genereted_id_info: GeneratedIdInfo
    ) -> GeneratedIdInfo:
        pass

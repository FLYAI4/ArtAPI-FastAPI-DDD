from abc import ABC, abstractmethod
from src.user.domain.entity import (
    UserReview,
    UserId,
    ContentName,
    ContentInfo
)


class UserRepositoryInterface(ABC):
    @abstractmethod
    def insert_user_review(
        postgre_session, user_review: UserReview
    ) -> UserId:
        pass

    @abstractmethod
    def delete_user_review(
        postgre_session, user_review: UserReview
    ) -> UserId:
        pass

    @abstractmethod
    def get_text_content(
        mongo_session, content_name: ContentName
    ) -> ContentInfo:
        pass

    @abstractmethod
    def get_coord_content(
        mongo_session, content_name: ContentName
    ) -> ContentInfo:
        pass

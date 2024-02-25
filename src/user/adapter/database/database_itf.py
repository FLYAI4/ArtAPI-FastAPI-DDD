from abc import ABC, abstractmethod
from src.user.domain.entity import UserReview, UserId


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

from sqlalchemy import select
from src.user.adapter.database.database_itf import UserRepositoryInterface
from src.user.domain.entity import UserReview, UserId
from src.shared_kernel.domain.exception import DBError
from src.shared_kernel.domain.error_code import RepositoryError
from src.user.infra.database.model import Review
from src.user.domain.entity import ContentInfo, ContentName


class UserRepository(UserRepositoryInterface):
    def insert_user_review(
            postgre_session, user_review: UserReview
    ) -> UserId:
        try:
            obj = Review(
                id=user_review.id,
                image_name=user_review.image_name,
                like_status=user_review.like_status,
                review_content=user_review.review_content
            )
            with postgre_session as session:
                session.add(obj)
                session.commit()
            return UserId(
                id=user_review.id
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def delete_user_review(
            postgre_session, user_review: UserReview
    ) -> UserId:
        try:
            with postgre_session as session:
                sql = select(Review).filter(
                    Review.image_name == user_review.image_name
                )
                obj = session.execute(sql).scalars().first()
                if obj:
                    session.delete(obj)
                session.commit()
            return UserId(
                id=user_review.id
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def get_text_content(
            mongo_session, content_name: ContentName
    ) -> ContentInfo:
        try:
            collection = mongo_session["user_generated"]
            document = collection.find_one(
                {"_id": content_name.image_name})
            return ContentInfo(
                tag="text",
                data=document["text_content"]
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def get_coord_content(
            mongo_session, content_name: ContentName
    ) -> ContentInfo:
        try:
            collection = mongo_session["user_generated"]
            document = collection.find_one(
                {"_id": content_name.image_name})
            return ContentInfo(
                tag="coord",
                data=document["coord_content"]
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

from sqlalchemy import select
from src.user.adapter.database.database_itf import UserRepositoryInterface
from src.user.domain.entity import GeneratedContentModel, GeneratedIdInfo, UserContent
from src.shared_kernel.domain.exception import DBError
from src.shared_kernel.domain.error_code import RepositoryError
from src.user.infra.database.model import Content


class UserRepository(UserRepositoryInterface):
    def insert_content(
            mongo_session,
            generated_content: GeneratedContentModel
    ) -> GeneratedIdInfo:
        try:
            generated_data = {
                "_id": generated_content.generated_id,
                "user_id": generated_content.id,
                "text_content": generated_content.text_content,
                "coord_content": generated_content.coord_content,
            }
            collection = mongo_session["user_generated"]

            result = collection.insert_one(generated_data)
            return GeneratedIdInfo(
                id=generated_content.id,
                generated_id=result.inserted_id
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def insert_generated_id(
        postgre_session, genereted_id_info: GeneratedIdInfo
    ) -> GeneratedIdInfo:
        try:
            obj = Content(
                id=genereted_id_info.id,
                generated_id=genereted_id_info.generated_id
            )

            with postgre_session as session:
                session.add(obj)
                session.commit()
            return genereted_id_info
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def delete_generated_id(
        postgre_session, genereted_id_info: GeneratedIdInfo
    ) -> GeneratedIdInfo:
        try:
            with postgre_session as session:
                sql = select(Content).filter(
                    Content.generated_id == genereted_id_info.generated_id
                    )
                obj = session.execute(sql).scalar_one()
                if obj:
                    session.delete(obj)
                session.commit()
                return genereted_id_info
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def update_user_content_status(
            postgre_session, generated_id_info: GeneratedIdInfo
    ) -> GeneratedIdInfo:
        try:
            with postgre_session as session:
                sql = select(Content).filter(
                    Content.generated_id == generated_id_info.generated_id
                )
                obj = session.execute(sql).scalar_one()
                obj.status = True
                session.commit()
                return generated_id_info
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def get_user_content(
            postgre_session, generated_id_info: GeneratedIdInfo
    ) -> UserContent:
        try:
            with postgre_session as session:
                sql = select(Content).filter(
                    Content.generated_id == generated_id_info.generated_id
                    )
                obj = session.execute(sql).scalar_one()
                return UserContent(
                    id=obj.id,
                    generated_id=obj.generated_id,
                    status=obj.status
                )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

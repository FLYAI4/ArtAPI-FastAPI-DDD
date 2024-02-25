from sqlalchemy import select
from src.admin.domain.entity import GeneratedContent, GeneratedContentName
from src.admin.adapter.database.database_abs import AdminRepositoryInterface
from src.admin.infra.database.model import Content
from src.shared_kernel.domain.exception import DBError
from src.shared_kernel.domain.error_code import RepositoryError


class AdminRepository(AdminRepositoryInterface):
    def insert_content(
            postgre_session, generated_content: GeneratedContent
    ) -> GeneratedContentName:
        try:
            obj = Content(
                image_name=generated_content.image_name,
                origin_image=generated_content.origin_image,
                audio_content=generated_content.audio_content,
                video_content=generated_content.video_content
            )

            with postgre_session as session:
                session.add(obj)
                session.commit()
            return GeneratedContentName(
                image_name=generated_content.image_name
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def delete_content(
            postgre_session, generated_content_name: GeneratedContentName
    ) -> GeneratedContentName:
        try:
            with postgre_session as session:
                sql = select(Content).filter(
                    Content.image_name == generated_content_name.image_name
                )
                obj = session.execute(sql).scalar_one()
                if obj:
                    session.delete(obj)
                session.commit()
                return generated_content_name
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

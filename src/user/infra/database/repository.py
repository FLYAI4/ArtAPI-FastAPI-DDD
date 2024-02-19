from src.user.adapter.database.database_itf import UserRepositoryInterface
from src.user.domain.entity import GeneratedContentModel, GeneratedIdInfo
from src.shared_kernel.domain.exception import DBError
from src.shared_kernel.domain.error_code import RepositoryError


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

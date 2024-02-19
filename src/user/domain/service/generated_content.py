import os
from src.user.domain.entity import GeneratedIdInfo
from src.user.domain.util.local_file import find_storage_path


class GeneratedContentService:
    def create_generated_content(self, user_id_info: GeneratedIdInfo):
        # load image from local
        origin_file = self.__find_user_origin_image(user_id_info.generated_id)

        # create generate content
        # gif, main content, coord content

        # image compress

        # save mongodb

        # save posgreSQL

        pass

    def __find_user_origin_image(generated_id: str) -> str:
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(storage_path, generated_id))
        origin_file = os.path.abspath(os.path.join(user_path, "origin_img.jpg"))
        return origin_file

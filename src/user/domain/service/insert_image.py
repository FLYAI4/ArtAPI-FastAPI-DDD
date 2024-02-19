import os
from datetime import datetime
from src.user.domain.entity import OriginImageInfo, FileInfo
from src.user.domain.util.local_file import (
    find_storage_path,
    create_folder_if_not_exists
    )


class InsertImageService:
    def insert_image(self, origin_image: OriginImageInfo) -> FileInfo:
        # set unique id
        user_unique_id = self.__generated_uniqnue_id(origin_image.id)
        origin_image.id = user_unique_id

        # make unique id folder
        storage_path = find_storage_path()
        user_path = os.path.abspath(os.path.join(
            storage_path, origin_image.id
            ))
        create_folder_if_not_exists(user_path)

        # save file
        user_file_path = os.path.abspath(os.path.join(
            user_path, "origin_img.jpg"
            ))
        with open(user_file_path, "wb") as f:
            f.write(origin_image.image_file)
        return FileInfo(unique_id=user_unique_id, path=user_file_path)

    @staticmethod
    def __generated_uniqnue_id(user_id: str):
        """Generate unique id according to API request."""
        id_prefix = user_id.split("@")[0]
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{id_prefix}"

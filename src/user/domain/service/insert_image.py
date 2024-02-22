import os
import io
from datetime import datetime
from PIL import Image
from src.user.domain.entity import OriginImageInfo, FileInfo
from src.user.domain.util.local_file import (
    find_storage_path,
    create_folder_if_not_exists
    )


class InsertImageService:
    def __init__(self) -> None:
        self.width = 510
        self.height = 680

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
        self.__resize_image(
            origin_image.image_file,
            user_file_path,
            self.width, self.height
        )
        return FileInfo(unique_id=user_unique_id, path=user_file_path)

    @staticmethod
    def __generated_uniqnue_id(user_id: str):
        """Generate unique id according to API request."""
        id_prefix = user_id.split("@")[0]
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{id_prefix}"

    @staticmethod
    def __resize_image(
        image_bytes: bytes,
        user_file_path: str,
        width: int, height: int
    ):
        image = Image.open(io.BytesIO(image_bytes))
        resized_image = image.resize((width, height))
        resized_image.save(user_file_path)

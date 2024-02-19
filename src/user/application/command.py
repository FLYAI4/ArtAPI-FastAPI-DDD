from fastapi import UploadFile
from src.user.domain.entity import FileInfo, OriginImageInfo
from src.user.domain.service.insert_image import InsertImageService


class UserCommandUseCase:
    def __init__(self) -> None:
        pass

    def insert_image(
            self, id: str, file: UploadFile
    ) -> FileInfo:
        # convert request to entity
        origin_image = OriginImageInfo(
            id=id,
            image_file=file.file.read()
        )

        # save local
        return InsertImageService().insert_image(origin_image)

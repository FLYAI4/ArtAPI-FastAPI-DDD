from src.user.adapter.rest.request import InsertImageRequest
from src.user.domain.entity import FileInfo, OriginImageInfo
from src.user.domain.service.insert_image import InsertImageService


class UserCommandUseCase:
    def __init__(self) -> None:
        pass

    def insert_image(self, request: InsertImageRequest) -> FileInfo:
        # convert request to entity
        origin_image = OriginImageInfo(
            id=request.id,
            image_file=request.image_file
        )

        # save local
        return InsertImageService().insert_image(origin_image)

from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.user.domain.entity import (
    FileInfo,
    OriginImageInfo
    )
from src.user.adapter.rest.request import GeneratedContentRequest
from src.user.domain.service.insert_image import InsertImageService
from src.user.infra.database.repository import UserRepository
from src.user.domain.exception import UserServiceError, UserApplicationError
from src.user.domain.errorcode import InsertImageError


class UserCommandUseCase:
    def __init__(
            self,
            mongo_session: any = None,
            postgre_session: Session = None
    ) -> None:
        self.mogno_session = mongo_session
        self.postgre_session = postgre_session

    async def insert_image(
            self, id: str, file: UploadFile
    ) -> FileInfo:
        try:
            # convert request to entity
            origin_image = OriginImageInfo(
                id=id,
                image_file=file.file.read()
            )

            # save local
            file_info = await InsertImageService().insert_image(origin_image)

            # save posgreSQL -> generated_id
            # generated_id_info = GeneratedIdInfo(
            #     id=id,
            #     generated_id=file_info.unique_id
            # )
            # UserRepository.insert_generated_id(
            #     self.postgre_session, generated_id_info)
            return file_info
        except UserServiceError as e:
            raise e
        except Exception as e:
            raise UserApplicationError(
                **InsertImageError.UnknownError.value, err=e)

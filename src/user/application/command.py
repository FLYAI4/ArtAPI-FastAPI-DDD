from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.user.domain.entity import (
    FileInfo,
    OriginImageInfo,
    GeneratedIdInfo,
    GeneratedContent
    )
from src.user.adapter.rest.request import GeneratedContentRequest
from src.user.domain.service.insert_image import InsertImageService
from src.user.domain.service.generated_content import GeneratedContentService
from src.user.infra.database.repository import UserRepository
from src.user.domain.entity import GeneratedContentModel
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

    def insert_image(
            self, id: str, file: UploadFile
    ) -> FileInfo:
        try:
            # convert request to entity
            origin_image = OriginImageInfo(
                id=id,
                image_file=file.file.read()
            )

            # save local
            return InsertImageService().insert_image(origin_image)
        except UserServiceError as e:
            raise e
        except Exception as e:
            raise UserApplicationError(
                **InsertImageError.UnknownError.value, err=e)

    async def generate_content(
            self, id: str, requset: GeneratedContentRequest
    ):
        # convert request to entity
        generated_id_info = GeneratedIdInfo(
            id=id,
            generated_id=requset.generated_id
        )

        # create generated content
        async for content in GeneratedContentService().create_generated_content(
            generated_id_info
        ):
            if content.tag == "gif":
                yield f"{content.tag}: {content.data}\n".encode()
            if content.tag == "text":
                text_content = GeneratedContent(
                    generated_id=generated_id_info.generated_id,
                    tag=content.tag,
                    content=content.data
                )
            if content.tag == "coord":
                coord_content = GeneratedContent(
                    generated_id=generated_id_info.generated_id,
                    tag=content.tag,
                    content=content.data
                )
            if content.tag == "audio":
                audio_content = GeneratedContent(
                    generated_id=generated_id_info.generated_id,
                    tag=content.tag,
                    content=content.data
                )
                # save audio content to local
                await GeneratedContentService().save_audio_content_to_local(
                    generated_id_info, audio_content
                )

        # save mongodb -> text, coord DB 저장
        generated_content = GeneratedContentModel(
            id=generated_id_info.id,
            generated_id=generated_id_info.generated_id,
            text_content=text_content.content,
            coord_content=coord_content.content
        )
        generated_id_info = UserRepository.insert_content(
            self.mogno_session, generated_content
            )

        # save posgreSQL -> generated_id
        generated_id_info = UserRepository.insert_generated_id(
            self.postgre_session, generated_id_info
            )

        # 생성 완료 응답 -> finish
        yield f"finish: {generated_id_info.id}\n".encode()

from fastapi import UploadFile
from src.user.domain.entity import (
    FileInfo,
    OriginImageInfo,
    GeneratedIdInfo,
    GeneratedContent
    )
from src.user.adapter.rest.request import GeneratedContentRequest
from src.user.domain.service.insert_image import InsertImageService
from src.user.domain.service.generated_content import GeneratedContentService


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
                yield GeneratedContent(
                    generated_id=generated_id_info.generated_id,
                    tag=content.tag,
                    content=content.data
                )
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
                # audio content 로컬에 저장
                await GeneratedContentService().save_audio_content_to_local(
                    generated_id_info, audio_content
                )

                # 생성 완료 응답 -> finish

        print(text_content.content)
        print(coord_content.content)
        print(type(audio_content.content))

        # save mongodb -> text, coord DB 저장

        # save posgreSQL -> generated_id

        # 생성 완료 응답 -> finish

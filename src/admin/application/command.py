from fastapi import UploadFile
from azure.storage.blob import BlobServiceClient
from src.admin.domain.entity import (
    GeneratedContentName,
    OriginImageInfo,
    GeneratedContent,
    GeneratedTextContent
)
from src.admin.domain.service.generated_content import GeneratedContentService
from src.admin.infra.database.repository import AdminRepository


class AdminCommandUseCase:
    def __init__(
            self,
            mongo_session,
            azure_blob_session: BlobServiceClient
    ) -> None:
        self.mongo_session = mongo_session
        self.azure_blob_session = azure_blob_session

    async def generate_content(
            self,
            image_name: str,
            file: UploadFile
    ) -> GeneratedContentName:
        origin_image_info = OriginImageInfo(
            image_name=image_name,
            image_file=file.file.read()
        )

        # resize image
        resize_image = GeneratedContentService().resize_image(
            origin_image_info)

        # generate content
        generated_text_content = GeneratedTextContent(
            image_name=image_name
        )

        generated_content = GeneratedContent(
            image_name=image_name,
            origin_image=open(resize_image, "rb").read()
            )

        async for content in GeneratedContentService().generated_content(
            origin_image_info
        ):
            if content.tag == "text":
                generated_text_content.text_content = content.data
            if content.tag == "coord":
                generated_text_content.coord_content = content.data
            if content.tag == "audio":
                generated_content.audio_content = content.data
            if content.tag == "video":
                generated_content.video_content = content.data

        await GeneratedContentService().delete_resize_image(origin_image_info)

        # save mongo DB
        AdminRepository.insert_text_content(
            self.mongo_session, generated_text_content
        )

        # save azure blob storage
        return AdminRepository.insert_content(
            self.azure_blob_session, generated_content)

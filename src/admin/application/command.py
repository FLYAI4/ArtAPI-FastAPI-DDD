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
from src.admin.domain.errorcode import GeneratedContentsError
from src.admin.domain.exception import AdminServiceError, AdminApplicationError
from src.shared_kernel.domain.exception import DBError


class AdminCommandUseCase:
    def __init__(
            self,
            admin_repository: AdminRepository,
            generated_content_service: GeneratedContentService,
            mongo_session: any,
            azure_blob_session: BlobServiceClient
    ) -> None:
        self.admin_repository = admin_repository
        self.generated_content_service = generated_content_service
        self.mongo_session = mongo_session
        self.azure_blob_session = azure_blob_session

    async def generate_content(
            self,
            image_name: str,
            file: UploadFile
    ) -> GeneratedContentName:
        try:
            origin_image_info = OriginImageInfo(
                image_name=image_name,
                image_file=file.file.read()
            )

            # resize image
            resize_image = self.generated_content_service.resize_image(
                origin_image_info)

            # generate content
            generated_text_content = GeneratedTextContent(
                image_name=image_name
            )

            generated_content = GeneratedContent(
                image_name=image_name,
                origin_image=open(resize_image, "rb").read()
                )

            async for content in self.generated_content_service.generated_content(
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

            await self.generated_content_service.delete_resize_image(origin_image_info)

            # save mongo DB
            with self.mongo_session() as session:
                self.admin_repository.insert_text_content(
                    session, generated_text_content
                )

            # save azure blob storage
            with self.azure_blob_session() as session:
                generated_content_name = self.admin_repository.insert_content(
                    self.azure_blob_session, generated_content)
            return generated_content_name
        except (AdminServiceError, DBError) as e:
            raise e
        except Exception as e:
            raise AdminApplicationError(**GeneratedContentsError.UnKnowError.value, err=e)

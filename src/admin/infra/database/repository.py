import os
from sqlalchemy import select
from src.admin.domain.entity import GeneratedContent, GeneratedContentName
from src.admin.adapter.database.database_abs import AdminRepositoryInterface
from src.shared_kernel.domain.exception import DBError
from src.shared_kernel.domain.error_code import RepositoryError


class AdminRepository(AdminRepositoryInterface):
    def insert_content(
            azure_blob_session, generated_content: GeneratedContent
    ) -> GeneratedContentName:
        try:
            container_name = "generated-content"

            # save image content
            image_file = os.path.join(generated_content.image_name, "origin_img.jpg")
            blob_client = azure_blob_session.get_blob_client(container_name, image_file)
            blob_client.upload_blob(generated_content.origin_image)

            # save audio content
            audio_file = os.path.join(generated_content.image_name, "main.mp3")
            blob_client = azure_blob_session.get_blob_client(container_name, audio_file)
            blob_client.upload_blob(generated_content.audio_content)

            # save video content
            video_file = os.path.join(generated_content.image_name, "video.mp4")
            blob_client = azure_blob_session.get_blob_client(container_name, video_file)
            blob_client.upload_blob(generated_content.video_content)

            return GeneratedContentName(
                image_name=generated_content.image_name
            )
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

    def delete_content(
            azure_blob_session, generated_content_name: GeneratedContentName
    ) -> GeneratedContentName:
        try:
            container_name = "generated-content"

            # delete contents
            blob_list = azure_blob_session.get_container_client(container_name).list_blobs(
                name_starts_with=generated_content_name.image_name)
            for blob in blob_list:
                blob_client = azure_blob_session.get_blob_client(container_name, blob.name)
                blob_client.delete_blob()
            return generated_content_name
        except Exception as e:
            raise DBError(**RepositoryError.DBProcess.value, err=e)

from azure.storage.blob import BlobServiceClient
from fastapi import APIRouter, UploadFile, File, Depends, Header
from src.admin.adapter.rest.response import GeneratedContentResponse
from src.admin.application.command import AdminCommandUseCase
from src.shared_kernel.infra.database.connection import MongoManager, BlobStorageManager


admin = APIRouter(prefix="/admin")


@admin.post("/content")
async def generate_content(
    file: UploadFile = File(...),
    imagename: str = Header(...),
    mongo_session: any = Depends(MongoManager.get_session),
    azure_blob_session: BlobServiceClient = Depends(
        BlobStorageManager.get_session)
):
    command = AdminCommandUseCase(
        mongo_session, azure_blob_session
    )
    result = await command.generate_content(imagename, file)
    return GeneratedContentResponse(
        generated_content_name=result
    ).build()

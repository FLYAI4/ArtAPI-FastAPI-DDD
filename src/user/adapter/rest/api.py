from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Header, Depends
from src.user.application.command import UserCommandUseCase
from src.user.adapter.rest.response import (
    SignUpUserResponse,
    GetContentResponse,
    GetCoordContentResponse,
    GetVideoContentResponse,
    PostContentReviewResponse
)
from src.shared_kernel.infra.database.connection import (
    MongoManager,
    PostgreManager,
    BlobStorageManager
)
from src.shared_kernel.infra.fastapi.auth import get_current_user
from src.user.adapter.rest.request import InsertUserContentReview

user = APIRouter(prefix="/user")


@user.post('/image')
async def insert_image(
    id: str = Header(),
    file: UploadFile = File(...),
    postgre_session: Session = Depends(PostgreManager.get_session),
    auth: str = Depends(get_current_user)
):
    command = UserCommandUseCase(postgre_session=postgre_session)
    result = await command.insert_image(id, file)
    return SignUpUserResponse(file_info=result).build()


@user.get('/content')
async def get_main_content(
    id: str = Header(),
    generated_id: str = Header(),
    mongo_session: any = Depends(MongoManager.get_session),
    azure_blob_session: any = Depends(BlobStorageManager.get_session),
    auth: str = Depends(get_current_user)
):
    command = UserCommandUseCase(
        mongo_session=mongo_session,
        azure_blob_session=azure_blob_session
        )
    result = await command.get_main_content(generated_id)
    return GetContentResponse(content=result).build()


@user.get('/content/coord')
async def get_coord_content(
    id: str = Header(),
    generated_id: str = Header(),
    mongo_session: any = Depends(MongoManager.get_session),
    auth: str = Depends(get_current_user)
):
    command = UserCommandUseCase(mongo_session=mongo_session)
    result = await command.get_coord_content(generated_id)
    return GetCoordContentResponse(content=result).build()


@user.get('/content/video')
async def get_video_content(
    id: str = Header(),
    generated_id: str = Header(),
    azure_blob_session: any = Depends(BlobStorageManager.get_session),
    auth: str = Depends(get_current_user)
):
    command = UserCommandUseCase(azure_blob_session=azure_blob_session)
    result = await command.get_video_content(generated_id)
    return GetVideoContentResponse(content=result).build()


@user.post('/content/review')
async def insert_user_content_review(
    request: InsertUserContentReview,
    id: str = Header(),
    generated_id: str = Header(),
    postgre_session: Session = Depends(PostgreManager.get_session),
    auth: str = Depends(get_current_user)
):
    command = UserCommandUseCase(postgre_session=postgre_session)
    result = await command.insert_user_content_review(
        id=id,
        generated_id=generated_id,
        request=request
    )
    return PostContentReviewResponse(content=result).build()

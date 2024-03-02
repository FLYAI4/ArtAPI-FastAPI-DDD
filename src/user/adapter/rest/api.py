from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, UploadFile, File, Header, Depends
from src.user.application.command import UserCommandUseCase
from src.user.adapter.rest.response import (
    SignUpUserResponse,
    GetContentResponse,
    GetCoordContentResponse,
    GetVideoContentResponse,
    PostContentReviewResponse
)
from src.shared_kernel.infra.fastapi.auth import get_current_user
from src.user.adapter.rest.request import InsertUserContentReview
from src.shared_kernel.infra.container import AppContainer

user = APIRouter(prefix="/user")


@user.post('/image')
@inject
async def insert_image(
    id: str = Header(),
    file: UploadFile = File(...),
    user_command: UserCommandUseCase = Depends(
        Provide[AppContainer.user.user_command]
    ),
    auth: str = Depends(get_current_user)
):
    result = await user_command.insert_image(id, file)
    return SignUpUserResponse(file_info=result).build()


@user.get('/content')
@inject
async def get_main_content(
    id: str = Header(),
    generated_id: str = Header(),
    user_command: UserCommandUseCase = Depends(
        Provide[AppContainer.user.user_command]
    ),
    auth: str = Depends(get_current_user)
):
    result = await user_command.get_main_content(generated_id)
    return GetContentResponse(content=result).build()


@user.get('/content/coord')
@inject
async def get_coord_content(
    id: str = Header(),
    generated_id: str = Header(),
    user_command: UserCommandUseCase = Depends(
        Provide[AppContainer.user.user_command]
    ),
    auth: str = Depends(get_current_user)
):
    result = await user_command.get_coord_content(generated_id)
    return GetCoordContentResponse(content=result).build()


@user.get('/content/video')
@inject
async def get_video_content(
    id: str = Header(),
    generated_id: str = Header(),
    user_command: UserCommandUseCase = Depends(
        Provide[AppContainer.user.user_command]
    ),
    auth: str = Depends(get_current_user)
):
    result = await user_command.get_video_content(generated_id)
    return GetVideoContentResponse(content=result).build()


@user.post('/content/review')
@inject
async def insert_user_content_review(
    request: InsertUserContentReview,
    id: str = Header(),
    generated_id: str = Header(),
    user_command: UserCommandUseCase = Depends(
        Provide[AppContainer.user.user_command]
    ),
    auth: str = Depends(get_current_user)
):
    result = await user_command.insert_user_content_review(
        id=id,
        generated_id=generated_id,
        request=request
    )
    return PostContentReviewResponse(content=result).build()

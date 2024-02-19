from fastapi import APIRouter, UploadFile, File, Header
from src.user.application.command import UserCommandUseCase
from src.user.adapter.rest.response import SignUpUserResponse


user = APIRouter(prefix="/user")


@user.post('/image')
async def insert_image(
    id: str = Header(),
    token: str = Header(),
    file: UploadFile = File(...),
):
    command = UserCommandUseCase()
    result = command.insert_image(id, file)
    return SignUpUserResponse(file_info=result).build()

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, UploadFile, File, Depends, Header
from src.admin.adapter.rest.response import GeneratedContentResponse
from src.admin.application.command import AdminCommandUseCase
from src.shared_kernel.infra.container import AppContainer

admin = APIRouter(prefix="/admin")


@admin.post("/content")
@inject
async def generate_content(
    file: UploadFile = File(...),
    imagename: str = Header(...),
    admin_command: AdminCommandUseCase = Depends(
        Provide[AppContainer.admin.admin_command])
):
    result = await admin_command.generate_content(imagename, file)
    return GeneratedContentResponse(
        generated_content_name=result
    ).build()

import pydantic
from src.user.domain.entity import (
    FileInfo,
    MainContent,
    CoordContent,
    VideoContent,
    UserId
)
from src.shared_kernel.infra.fastapi.util import make_response
from src.shared_kernel.infra.fastapi.logger import Logger
from dataclasses import asdict


class SignUpUserResponse(pydantic.BaseModel):
    file_info: FileInfo

    def build(self):
        Logger("INFO", "Success generated contents")
        return make_response(
            {"generated_id": self.file_info.image_name}
        )


class GetContentResponse(pydantic.BaseModel):
    content: MainContent

    def build(self):
        Logger("INFO", "Success get text content")
        return make_response(asdict(self.content))


class GetCoordContentResponse(pydantic.BaseModel):
    content: CoordContent

    def build(self):
        Logger("INFO", "Success get coord content")
        return make_response(asdict(self.content))


class GetVideoContentResponse(pydantic.BaseModel):
    content: VideoContent

    def build(self):
        Logger("INFO", "Success get video content")
        return make_response(asdict(self.content))


class PostContentReviewResponse(pydantic.BaseModel):
    content: UserId

    def build(self):
        Logger("INFO", "Success post review content")
        return make_response(
            {"id": self.content.id}
        )

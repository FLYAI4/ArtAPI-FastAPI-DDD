import os
import pytest
from fastapi import UploadFile
from src.user.application.command import UserCommandUseCase
from src.user.adapter.rest.request import GeneratedContentRequest
from src.shared_kernel.infra.database.connection import (
    MongoManager,
    PostgreManager
)

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def command():
    yield UserCommandUseCase(
        MongoManager.get_session(),
        PostgreManager.get_session()
        )


def test_can_insert_image_with_valid(command):
    with open(IMAGE_PATH, "rb") as f:
        file = UploadFile(file=f)
        result = command.insert_image(ID, file)

    assert result.unique_id.split("_")[-1] == ID.split("@")[0]
    assert os.path.isfile(result.path)


@pytest.mark.asyncio
async def test_can_generate_content_with_valid(command):
    with open(IMAGE_PATH, "rb") as f:
        file = UploadFile(file=f)
        result = command.insert_image(ID, file)

    assert os.path.isfile(result.path)

    # given : 유효한 payload
    mockup = GeneratedContentRequest(
        generated_id=result.unique_id
    )

    # when : 콘텐츠 생성 요청
    async for chunk in command.generate_content(ID, mockup):
        assert chunk.generated_id == result.unique_id
        assert chunk.tag in ["gif", "finish"]

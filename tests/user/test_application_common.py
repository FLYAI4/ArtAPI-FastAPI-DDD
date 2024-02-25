import os
import pytest
import time
import json
from fastapi import UploadFile
from src.user.application.command import UserCommandUseCase
from src.user.domain.exception import UserServiceError
from src.shared_kernel.infra.database.connection import (
    MongoManager,
    PostgreManager,
    BlobStorageManager
)

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))
GENERATED_ID = "4.jpg"


@pytest.fixture
def command():
    yield UserCommandUseCase(
        MongoManager.get_session(),
        PostgreManager.get_session(),
        BlobStorageManager.get_session()
        )


@pytest.mark.asyncio
async def test_can_insert_image_with_valid(command):
    with open(IMAGE_PATH, "rb") as f:
        file = UploadFile(file=f)
        result = await command.insert_image(ID, file)

    assert result.image_name == "4.jpg"


@pytest.mark.asyncio
async def test_cannot_insert_image_with_no_match_image(command):
    time.sleep(1)
    wrong_image_path = os.path.abspath(os.path.join(test_img_path, "wrong.jpg"))
    with pytest.raises(UserServiceError):
        with open(wrong_image_path, "rb") as f:
            file = UploadFile(file=f)
            await command.insert_image(ID, file)


@pytest.mark.asyncio
async def test_can_get_main_content_with_valid(command):
    result = await command.get_main_content(GENERATED_ID)

    assert result.resize_image
    assert result.audio_content
    print(result.text_content)


@pytest.mark.asyncio
async def test_can_get_coord_content_with_valid(command):
    result = await command.get_coord_content(GENERATED_ID)

    assert result.coord_content
    json_data = json.loads(result.coord_content)
    print(json_data)


@pytest.mark.asyncio
async def test_can_get_video_content_with_valid(command):
    result = await command.get_video_content(GENERATED_ID)

    assert result.video_content

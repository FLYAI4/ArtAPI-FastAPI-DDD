import os
import pytest
from fastapi import UploadFile
from src.user.application.demo import UserCommandDemo

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "demo@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))
GENERATED_ID = "demo"


@pytest.fixture
def command():
    yield UserCommandDemo()


def test_can_demo_insert_image_with_valid(command):
    with open(IMAGE_PATH, "rb") as f:
        file = UploadFile(file=f)
        result = command.demo_insert_image(ID, file)

    assert result.unique_id.split("_")[-1] == ID.split("@")[0]


@pytest.mark.asyncio
async def test_can_deomo_generate_content_with_valid(command):

    async for chunk in command.demo_generate_content(GENERATED_ID):
        assert chunk.decode().split(":")[0] in ["gif", "finish"]


def test_demo_get_text_audio_content(command):
    result = command.demo_get_text_audio_content(GENERATED_ID)

    assert result["text_content"]
    assert result["audio_content"]


def test_demo_get_coord_content(command):
    result = command.demo_get_coord_content(GENERATED_ID)
    assert result["나무"]["좌표"]
    assert result["나무"]["내용"]


def test_demo_get_video_content(command):
    result = command.demo_get_video_content(GENERATED_ID)
    assert result["video_content"]

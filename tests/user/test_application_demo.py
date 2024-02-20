import os
import pytest
from fastapi import UploadFile
from src.user.application.demo import UserCommandDemo
from src.user.adapter.rest.request import GeneratedContentRequest

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "demo@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


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
    request = GeneratedContentRequest(
        generated_id="demo"
    )

    async for chunk in command.demo_generate_content(ID, request):
        assert chunk.decode().split(":")[0] in ["gif", "finish"]



import os
import pytest
from src.user.application.demo import UserCommandDemo
from src.user.adapter.rest.request import GeneratedContentRequest

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def command():
    yield UserCommandDemo()


@pytest.mark.asyncio
async def test_can_generate_content_with_valid(command):
    request = GeneratedContentRequest(
        generated_id="deme"
    )

    async for chunk in command.demo_generate_content(ID, request):
        assert chunk.decode().split(":")[0] in ["gif", "finish"]

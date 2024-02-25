import os
import pytest
from fastapi import UploadFile
from src.admin.application.command import AdminCommandUseCase
from src.shared_kernel.infra.database.connection import BlobStorageManager

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
IMAGE_NAME = "test.jpg"


@pytest.fixture
def command():
    yield AdminCommandUseCase(
        BlobStorageManager.get_session()
    )


@pytest.mark.asyncio
async def test_can_generated_content_with_valid(command):
    image_path = os.path.abspath(os.path.join(test_img_path, "origin_img.jpg"))

    with open(image_path, "rb") as f:
        file = UploadFile(file=f)
        result = await command.generate_content(IMAGE_NAME, file)

    assert result.image_name == IMAGE_NAME

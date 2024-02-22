import os
import pytest
from PIL import Image
import time
from src.user.domain.exception import UserServiceError
from src.user.domain.entity import OriginImageInfo
from src.user.domain.service.insert_image import InsertImageService

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.mark.asyncio
async def test_can_insert_image_with_valid():
    with open(IMAGE_PATH, "rb") as f:
        origin_image = OriginImageInfo(
            id=ID,
            image_file=f.read()
        )

    result = await InsertImageService().insert_image(origin_image)
    assert result.unique_id.split("_")[-1] == ID.split("@")[0]
    assert os.path.isfile(result.path)

    image = Image.open(result.path)
    image_width, image_height = image.size
    assert image_width == 510
    assert image_height == 680


@pytest.mark.asyncio
async def test_cannot_insert_image_with_wrong_image():
    time.sleep(1)
    wrong_image_path = os.path.abspath(os.path.join(test_img_path, "wrong.jpg"))
    with open(wrong_image_path, "rb") as f:
        origin_image = OriginImageInfo(
            id=ID,
            image_file=f.read()
        )

    with pytest.raises(UserServiceError):
        await InsertImageService().insert_image(origin_image)

import os
from PIL import Image
from src.user.domain.entity import OriginImageInfo
from src.user.domain.service.insert_image import InsertImageService

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


def test_can_insert_image_with_valid():
    with open(IMAGE_PATH, "rb") as f:
        origin_image = OriginImageInfo(
            id=ID,
            image_file=f.read()
        )

    result = InsertImageService().insert_image(origin_image)
    assert result.unique_id.split("_")[-1] == ID.split("@")[0]
    assert os.path.isfile(result.path)

    image = Image.open(result.path)
    image_width, image_height = image.size
    assert image_width == 510
    assert image_height == 680

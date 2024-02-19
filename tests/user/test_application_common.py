import os
from src.user.adapter.rest.request import InsertImageRequest
from src.user.application.command import UserCommandUseCase


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


def test_can_insert_image_with_valid():
    with open(IMAGE_PATH, "rb") as f:
        request = InsertImageRequest(
            id=ID,
            image_file=f.read()
        )

    result = UserCommandUseCase().insert_image(request)
    assert os.path.isfile(result.path)

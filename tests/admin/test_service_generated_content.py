import os
import pytest
from src.admin.domain.entity import OriginImageInfo
from src.admin.domain.service.generated_content import GeneratedContentService

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
IMAGE_NAME = "test.jpg"


@pytest.mark.asyncio
async def test_can_generate_content_with_valid():
    image_path = os.path.abspath(os.path.join(test_img_path, "origin_img.jpg"))

    with open(image_path, "rb") as f:
        origin_image_info = OriginImageInfo(
            image_name=IMAGE_NAME,
            image_file=f.read()
        )
    GeneratedContentService().resize_image(origin_image_info)

    async for chunck in GeneratedContentService().generated_content(origin_image_info):
        if chunck.tag == "text":
            assert chunck.data
        if chunck.tag == "video":
            assert chunck.data

    await GeneratedContentService().delete_resize_image(origin_image_info)

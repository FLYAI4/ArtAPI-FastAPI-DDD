import os
from src.user.domain.entity import GeneratedIdInfo, OriginImageInfo
from src.user.domain.service.insert_image import InsertImageService
from src.user.domain.service.generated_content import GeneratedContentService


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


def test_can_generated_content_with_valid():
    # 이미지 입력
    with open(IMAGE_PATH, "rb") as f:
        origin_image = OriginImageInfo(
            id=ID,
            image_file=f.read()
        )

    result = InsertImageService().insert_image(origin_image)
    assert result.unique_id.split("_")[-1] == ID.split("@")[0]
    assert os.path.isfile(result.path)

    # given : 유효한 데이터
    generated_id_info = GeneratedIdInfo(id=ID, generated_id=result.unique_id)

    text_content, coord_content = GeneratedContentService().create_generated_content(generated_id_info)
    print(text_content)
    print()
    print(coord_content)

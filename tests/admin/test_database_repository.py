import os
import pytest
import base64
from src.shared_kernel.infra.database.connection import BlobStorageManager, MongoManager
from src.admin.domain.entity import GeneratedContent, GeneratedTextContent
from src.admin.infra.database.repository import AdminRepository


admin_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(admin_path, "test_img"))

# Mock data
# IMAGE_NAME = "test.jpg"
# TEXT_CONTENT = b"hello helllo !!@#!$!@fgadfa"
# COORD_CONTENT = b'efbgaignpsadovcm1omfmdafmssv'



@pytest.fixture
def blob_session():
    yield BlobStorageManager.get_session()


@pytest.fixture
def mongo_session():
    yield MongoManager.get_session()


@pytest.fixture
def mockup():
    # origin_image
    origin_img = os.path.abspath(os.path.join(test_img_path, "origin_img.jpg"))
    audio_content = os.path.abspath(os.path.join(test_img_path, "main.mp3"))
    video_content = os.path.abspath(os.path.join(test_img_path, "video.mp4"))
    # with open(origin_img, "rb") as f:
    #     origin_img_data = f.read()

    yield GeneratedContent(
        image_name=IMAGE_NAME,
        origin_image=open(origin_img, "rb").read(),
        audio_content=open(audio_content, "rb").read(),
        video_content=open(video_content, "rb").read()
    )


# def test_can_insert_generated_content_with_valid(blob_session, mockup):
#     # given : 유효한 입력값
#     # when : DB 저장 요청
#     result = AdminRepository.insert_content(blob_session, mockup)

#     # then : 정상 응답
#     assert result.image_name == IMAGE_NAME

#     # 계정 삭제
#     result = AdminRepository.delete_content(blob_session, result)
#     assert result.image_name == IMAGE_NAME


def test_can_insert_text_content_with_valid(mongo_session):
    # given : 유효한 입력값
    
    IMAGE_NAME = "6.jpg"
    TEXT_CONTENT = '카쓰시카 호쿠사이는 에도 시대의 일본 예술가로, 우키요에 화가, 즉 판화가로 알려져 있습니다. 그는 1760년에 에도(지금의 도쿄)에서 태어났으며, 국제적으로 상징적인 작품인 "가나가와의 큰 파도"를 비롯한 "후지산 36경" 시리즈로 잘 알려져 있습니다. 호쿠사이의 작품은 우키요에 예술 형식에서 초상화 스타일로, 풍경, 식물 및 동물을 포함한 더 넓은 장르로 변화했습니다. 그의 작품은 일본뿐만 아니라 서양 예술, 특히 임프레션주의의 발전에도 영향을 미쳤습니다. "가나가와의 큰 파도"는 호쿠사이의 목공판화 기술에 대한 숙련도를 잘 보여주는 대표적인 작품입니다. 작품 구성은 다이내믹하며, 파도의 강렬한 곡선이 위협적이면서도 웅장한 움직임을 나타냅니다. 당시에는 프루시안 블루 피그먼트가 처음으로 도입되어 파도의 물거품에 흰색과 높은 대비를 만들어냈습니다. 작품에서는 작은 후지산이 배경에 나타나 파도의 규모와 대조를 이루며, 파도가 격동하는 반면에 고요하고 안정적으로 묘사되어 있습니다. 이 작품은 일본 미학에서 흔한 자연의 순간적인 아름다움을 담고 있습니다. 호쿠사이는 이 작품에 대량 생산이 가능한 목판 인쇄 기술을 선택했습니다. 이 스타일은 17세기부터 19세기까지 번성한 일본 예술 장르인 우키요에에 속합니다. 그의 작품은 중국의 회화 양식 및 네덜란드와 프랑스의 서양 예술에 영향을 받았습니다. "가나가와의 큰 파도"에서는 파도의 물뿌리를 나타내기 위해 부정한 공간을 사용하고, 파도의 거품은 호쿠사이의 정밀함과 질감 전달 능력을 보여줍니다. 이렇게 호쿠사이의 작품은 그의 예술적 진보와 독창성을 나타내며, 그의 영향력은 국내외 예술에 큰 발자취를 남겼습니다.'
    COORD_CONTENT = '{"위대한 파도": {"coord": [4, 44, 319, 398], "content": "위대한 파도는 작품의 중심에 있으며 자연의 힘을 상징합니다."}, "후지산": {"coord": [255, 416, 375, 519], "content": "후지산은 먼 거리에 평화롭고 작게 묘사되어 파도와 대조되는 규모감을 선사합니다."}, "배": {"coord": [8, 334, 222, 663], "content": "배들은 파도와 싸우는 모습으로 자연 속에서의 인간의 존재를 강조합니다."}}'

    mockup = GeneratedTextContent(
        image_name=IMAGE_NAME,
        text_content=TEXT_CONTENT.encode(),
        coord_content=COORD_CONTENT.encode()
    )

    # when : DB 저장 요청
    # print(mockup.text_content)
    # print(mockup.coord_content)
    # print(mockup.text_content.decode())
    # print(mockup.coord_content.decode())

    result = AdminRepository.delete_text_content(mongo_session, mockup)
    assert result.image_name == IMAGE_NAME

    result = AdminRepository.insert_text_content(
        mongo_session, mockup
    )

    # # then : 정상 응답
    assert result.image_name == IMAGE_NAME

    # 삭제
    # result = AdminRepository.delete_text_content(mongo_session, mockup)
    # assert result.image_name == IMAGE_NAME

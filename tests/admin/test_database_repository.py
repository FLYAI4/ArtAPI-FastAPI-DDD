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
    IMAGE_NAME = "1.jpg"
    TEXT_CONTENT = "이 작품은 평온한 바다 풍경을 중심으로 바다의 광활함과 물과 빛의 상호작용을 섬세하게 묘사하고 있습니다. 작가는 바다의 깊이와 넓이를 표현하기 위해 깊고 어두운 푸른색에서 시작하여 해안가로 접근하면서 점점 선명하고 생기 넘치는 파란색으로 전환되는 다양한 푸른색 톤을 활용했습니다. 파도의 거품이 만드는 흰 물결은 장면에 활력과 움직임을 더하며, 이는 하늘의 평온함과 대조를 이룹니다. 그럼에도 이 두 요소는 서로 완벽하게 조화를 이룹니다. 오일 또는 아크릴 페인트로 추정되는 매체는 색상의 부드러운 혼합과 파도의 생생한 질감을 효과적으로 전달합니다. 작품의 스타일은 현실적이면서도 인상파적인 터치를 가지고 있습니다. 이는 물에 대한 빛의 효과와 파도의 움직임을 정밀하게 묘사하기 보다는 자유로운 붓질로 표현하는 것에서 볼 수 있습니다. 이 작품은 낭만주의 시대의 해양화의 영향을 받았을 가능성이 있으며, 자연의 웅장한 힘에 중점을 둔 것으로 보입니다. 인상파적인 요소는 빛과 색에 대한 작가의 집중이 반영됩니다. 작가는 평화와 사색의 감정을 불러일으키기 위해 자연의 평온한 순간을 선택했습니다. 전경에 위치한 갈매기는 장면에 초점을 맞추고 바다의 웅장함을 강조하는 역할을 합니다. 그림의 주요 특징으로는 파란색 톤의 그라데이션, 바다와 하늘의 질감 대조, 그리고 지평선으로 사라지는 파도에 따른 크기 변화로 인한 깊이감을 들 수 있습니다. 이 모든 요소들이 합쳐져 이 작품의 매력을 더욱 돋보이게 합니다."
    COORD_CONTENT = ""

    mockup = GeneratedTextContent(
        image_name=IMAGE_NAME,
        text_content=base64.b64encode(TEXT_CONTENT),
        coord_content=base64.b64encode(COORD_CONTENT)
    )

    # when : DB 저장 요청
    result = AdminRepository.insert_text_content(
        mongo_session, mockup
    )

    # then : 정상 응답
    assert result.image_name == IMAGE_NAME

    # 삭제
    # result = AdminRepository.delete_text_content(mongo_session, mockup)
    # assert result.image_name == IMAGE_NAME

import os
import pytest
import base64
from src.shared_kernel.infra.database.connection import BlobStorageManager, MongoManager
from src.admin.domain.entity import GeneratedContent, GeneratedTextContent
from src.admin.infra.database.repository import AdminRepository


admin_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(admin_path, "test_img"))

# Mock data
IMAGE_NAME = "test.jpg"
TEXT_CONTENT = b"hello helllo !!@#!$!@fgadfa"
COORD_CONTENT = b'efbgaignpsadovcm1omfmdafmssv'



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
    result = AdminRepository.delete_text_content(mongo_session, mockup)
    assert result.image_name == IMAGE_NAME

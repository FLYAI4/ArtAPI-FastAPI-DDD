import os
import pytest
from src.shared_kernel.infra.database.connection import (
    PostgreManager,
    MongoManager,
    BlobStorageManager
)
from src.user.infra.database.repository import UserRepository
from src.user.domain.entity import UserReview, ContentName


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock
ID = "user2@naver.com"
IMAGE_NAME = "test.jpg"
REVIEW = "좋은 그림 입니다."

ALEADY_IMAGE_NAME = "check.jpg"


@pytest.fixture
def postgre_session():
    yield PostgreManager.get_session()


@pytest.fixture
def mongo_session():
    yield MongoManager.get_session()


@pytest.fixture
def azure_blob_session():
    yield BlobStorageManager.get_session()


def test_can_insert_user_review_with_valid(postgre_session):
    # given : 유효한 리뷰 정보
    mockup = UserReview(
        id=ID,
        image_name=IMAGE_NAME,
        like_status=True,
        review_content=REVIEW
    )

    # when : DB 저장
    result = UserRepository.insert_user_review(postgre_session, mockup)

    # then : 응답
    assert result.id == ID

    # 삭제
    result = UserRepository.delete_user_review(postgre_session, mockup)
    assert result.id == ID


def test_can_get_text_content_with_valud(mongo_session):
    # given : 유효한 리뷰 정보
    mockup = ContentName(
        image_name=ALEADY_IMAGE_NAME
    )

    # when : DB 조회
    result = UserRepository.get_text_content(mongo_session, mockup)

    # then : 응답
    assert result.tag == "text"
    print(result.data.decode('utf-8'))


def test_can_get_coord_content_with_valud(mongo_session):
    # given : 유효한 리뷰 정보
    mockup = ContentName(
        image_name=ALEADY_IMAGE_NAME
    )

    # when : DB 조회
    result = UserRepository.get_coord_content(mongo_session, mockup)

    # then : 응답
    assert result.tag == "coord"
    print(result.data.decode('utf-8'))


def test_can_get_origin_image_with_valid(azure_blob_session):
    # given : 유효한 이미지 정보
    mockup = ContentName(
        image_name=ALEADY_IMAGE_NAME
    )

    # when : DB 조회
    result = UserRepository.get_origin_image(azure_blob_session, mockup)

    # then : 응답
    assert result.tag == "origin_image"

    image_file = os.path.abspath(os.path.join(test_img_path, "hello.jpg"))
    with open(image_file, "wb") as f:
        f.write(result.data)


def test_can_get_audio_content_with_valid(azure_blob_session):
    # given : 유효한 이미지 정보
    mockup = ContentName(
        image_name=ALEADY_IMAGE_NAME
    )

    # when : DB 조회
    result = UserRepository.get_audio_content(azure_blob_session, mockup)

    # then : 응답
    assert result.tag == "audio"

    image_file = os.path.abspath(os.path.join(test_img_path, "main.mp3"))
    with open(image_file, "wb") as f:
        f.write(result.data)


def test_can_get_video_content_with_valid(azure_blob_session):
    # given : 유효한 이미지 정보
    mockup = ContentName(
        image_name=ALEADY_IMAGE_NAME
    )

    # when : DB 조회
    result = UserRepository.get_video_content(azure_blob_session, mockup)

    # then : 응답
    assert result.tag == "video"

    image_file = os.path.abspath(os.path.join(test_img_path, "video.mp4"))
    with open(image_file, "wb") as f:
        f.write(result.data)

import pytest
from src.shared_kernel.infra.database.connection import (
    PostgreManager,
    MongoManager
)
from src.user.infra.database.repository import UserRepository
from src.user.domain.entity import UserReview, ContentName

ID = "user2@naver.com"
IMAGE_NAME = "test.jpg"
REVIEW = "좋은 그림 입니다."

ALEADY_IMAGE_NAME = "check.jpg"

@pytest.fixture
def postgre_session():
    return PostgreManager.get_session()


@pytest.fixture
def mongo_session():
    return MongoManager.get_session()


# def test_can_insert_user_review_with_valid(postgre_session):
#     # given : 유효한 리뷰 정보
#     mockup = UserReview(
#         id=ID,
#         image_name=IMAGE_NAME,
#         like_status=True,
#         review_content=REVIEW
#     )

#     # when : DB 저장
#     result = UserRepository.insert_user_review(postgre_session, mockup)

#     # then : 응답
#     assert result.id == ID

#     # 삭제
#     result = UserRepository.delete_user_review(postgre_session, mockup)
#     assert result.id == ID


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

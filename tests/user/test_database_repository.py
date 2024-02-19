import pytest
from datetime import datetime
from src.shared_kernel.infra.database.connection import MongoManager
from src.user.infra.database.repository import UserRepository
from src.user.domain.entity import GeneratedContentModel

COLLECTION_NAME = "user_generated"
ID = "user2@naver.com"
TEXT_CONTENT = "hello helllo !!@#!$!@fgadfa"
COORD_CONTENT = 'efgaignpsadovcm1omfmdafmssv'

current_time = datetime.now()
timestamp = current_time.strftime("%Y%m%d_%H%M%S")


@pytest.fixture
def session():
    return MongoManager.get_session()


def test_can_insert_content_with_valid(session):
    # given : 유효한 계정
    generated_id = timestamp + "_" + ID
    generate_content = GeneratedContentModel(
        id=ID,
        generated_id=generated_id,
        text_content=TEXT_CONTENT,
        coord_content=COORD_CONTENT
    )

    # when : DB 저장 요청
    result = UserRepository.insert_content(session, generate_content)

    # then : 정상 응답
    assert result.id == ID
    assert result.generated_id == generated_id

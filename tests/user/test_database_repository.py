import pytest
from datetime import datetime
from src.shared_kernel.infra.database.connection import MongoManager, PostgreManager
from src.user.infra.database.repository import UserRepository
from src.user.domain.entity import GeneratedContentModel, GeneratedIdInfo

COLLECTION_NAME = "user_generated"
ID = "user2@naver.com"
TEXT_CONTENT = "hello helllo !!@#!$!@fgadfa"
COORD_CONTENT = 'efgaignpsadovcm1omfmdafmssv'

current_time = datetime.now()
timestamp = current_time.strftime("%Y%m%d_%H%M%S")


@pytest.fixture
def mongo_session():
    return MongoManager.get_session()

@pytest.fixture
def postgre_session():
    return PostgreManager.get_session()


def test_can_insert_content_with_valid(mongo_session):
    # given : 유효한 계정
    generated_id = timestamp + "_" + ID
    generate_content = GeneratedContentModel(
        id=ID,
        generated_id=generated_id,
        text_content=TEXT_CONTENT,
        coord_content=COORD_CONTENT
    )

    # when : DB 저장 요청
    result = UserRepository.insert_content(mongo_session, generate_content)

    # then : 정상 응답
    assert result.id == ID
    assert result.generated_id == generated_id


def test_can_insert_generated_id(postgre_session):
    # 유효한 계정
    generated_id = timestamp + "_" + ID
    generated_info = GeneratedIdInfo(
        id=ID,
        generated_id=generated_id
    )

    # when : DB 저장 요청
    result = UserRepository.insert_generated_id(postgre_session, generated_info)

    # then : 정상 응답
    assert result.id == ID
    assert result.generated_id == generated_id

    # 데이터 삭제
    result = UserRepository.delete_generated_id(postgre_session, generated_info)
    assert result.id == ID


def test_can_update_user_content_status(postgre_session):
    # given : 유효한 계정
    generated_id = timestamp + "_" + ID
    generated_info = GeneratedIdInfo(
        id=ID,
        generated_id=generated_id
    )

    result = UserRepository.insert_generated_id(postgre_session, generated_info)
    assert result.id == ID
    assert result.generated_id == generated_id

    result = UserRepository.get_user_content(postgre_session, generated_info)
    assert not result.status

    # when : user content 상태 변경
    result = UserRepository.update_user_content_status(postgre_session, generated_info)
    assert result.id == ID
    assert result.generated_id == generated_id

    # then : 상태 변경
    result = UserRepository.get_user_content(postgre_session, generated_info)
    assert result.status

    # 데이터 삭제
    result = UserRepository.delete_generated_id(postgre_session, generated_info)
    assert result.id == ID

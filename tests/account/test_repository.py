import uuid
import pytest
import base64
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo, UserInfo
from src.shared_kernel.domain.exception import DBError

# Mock data
ID = "test@naver.com"
PASSWORD = base64.b64encode(bytes("test1234", 'utf-8'))
NAME = "kim"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def mockup():
    yield AccountInfo(
        id=ID,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )


@pytest.fixture
def session():
    yield PostgreManager.get_session()

def test_account_repository_can_insert_user_account(mockup, session):
    # given : 유효한 유저 정보
    unique_id = ID + str(uuid.uuid4())[:10]
    mockup.id = unique_id

    # when : DB에 데이터 입력 요청
    result = AccountRepository.insert_user_account(session, mockup)

    # then : result.id
    assert result.id == unique_id

    # when : DB 데이터 확인
    user_info = UserInfo(id=unique_id)
    result = AccountRepository.get_user_account(session, user_info)

    # then : 데이터 정상적으로 입력 되었는지 확인
    assert result.id == unique_id
    assert result.password == PASSWORD
    assert result.name == NAME
    assert result.gender == GENDER
    assert result.age == AGE
    assert result.status

    result = AccountRepository.delete_user_account(session, user_info)
    assert result.id == unique_id


def test_account_repository_cannot_get_user_account(session):
    # given : DB에 없는 조회할 유저 ID
    WRONG_ID = "wrong_id"
    user_info = UserInfo(id=WRONG_ID)

    # then : DBError
    with pytest.raises(DBError):
        # when : DB 데이터 확인
        AccountRepository.get_user_account(session, user_info)


def test_account_repository_can_get_all_user_account(session, mockup):
    # given : 생성된 계정 존재
    unique_id = ID + str(uuid.uuid4())[:10]
    mockup.id = unique_id

    result = AccountRepository.insert_user_account(session, mockup)

    assert result.id == unique_id

    # when : DB에 데이터 전체 조회
    result = AccountRepository.get_all_user_account(session)

    # then : 조회된 데이터 확인
    assert len(result) > 0
    assert any(r.id == unique_id for r in result)

    user_info = UserInfo(id=unique_id)
    result = AccountRepository.delete_user_account(session, user_info)
    assert result.id == unique_id

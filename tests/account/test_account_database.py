import uuid
import pytest
import base64
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo

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

    # then : 데이터 정상적으로 입력 되었는지 확인
    assert result.id == unique_id

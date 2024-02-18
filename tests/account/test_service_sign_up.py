import pytest
import base64
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo, UserInfo
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.exception import UserError

# Mock data
PASSWORD = "test1234"
NAME = "별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def session():
    yield PostgreManager.get_session()


def test_cannot_sign_up_wrong_email_with_existence_user(session):
    # given : 이미 가입된 Email
    unique_id = "accountservice1@naver.com"
    mockup = AccountInfo(
        id=unique_id,
        password=base64.b64encode(bytes("test1234", 'utf-8')),
        name=NAME,
        gender=GENDER,
        age=AGE
    )
    result = AccountRepository.insert_user_account(session, mockup)
    assert result.id == unique_id

    # when : 가입 요청
    with pytest.raises(UserError):
        SignUpService().sign_up(session, mockup)

    # 계정 삭제
    user_info = UserInfo(id=unique_id)
    result = AccountRepository.delete_user_account(session, user_info)
    assert result.id == unique_id

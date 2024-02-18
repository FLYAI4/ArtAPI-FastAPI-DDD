import pytest
import base64
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import AccountInfo, UserInfo
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.exception import UserError
from src.account.domain.util.cipher import CipherManager

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
        SignUpService().sign_up_user(session, mockup)

    # 계정 삭제
    user_info = UserInfo(id=unique_id)
    result = AccountRepository.delete_user_account(session, user_info)
    assert result.id == unique_id


def test_can_sign_up_user_with_valid_user(session):
    # given : 유효한 계정
    unique_id = "accountservice1@naver.com"
    mockup = AccountInfo(
        id=unique_id,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )

    # when : 가입 요청
    result = SignUpService().sign_up_user(session, mockup)

    # then : 비밀번호 암호화
    assert result.id == unique_id
    encrypt_password = CipherManager().encrypt_password(PASSWORD)
    assert result.password == encrypt_password

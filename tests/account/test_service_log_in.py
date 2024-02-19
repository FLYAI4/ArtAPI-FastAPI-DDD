import pytest
import base64
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.domain.service.log_in import LogInService
from src.account.domain.service.sign_up import SignUpService
from src.account.infra.database.repository import AccountRepository
from src.account.application.command import AccountCommandUseCase
from src.account.domain.entity import AccountInfo, UserInfo
from src.account.domain.exception import UserError


# Mock data
ID = "accountservice1@naver.com"
PASSWORD = "test1234"
NAME = "별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def session():
    yield PostgreManager.get_session()


def test_cannot_log_in_with_non_existence(session):
    # given : 존재 하지 않는 계정 로그인 요청
    mockup = UserInfo(
        id="Wrong_id@naver.com",
        password=PASSWORD
    )
    # then : 예외 발생
    with pytest.raises(UserError):
        # when : 로그인 요청
        LogInService().log_in_user(session, mockup)


def test_cannot_log_in_with_wrong_password(session):
    # given : 존재하는 계정 + 틀린 비밀번호
    mockup = AccountInfo(
        id=ID,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )

    command = AccountCommandUseCase(SignUpService, AccountRepository, session)
    result = command.sign_up_user(mockup)

    assert result.id == ID

    mockup = UserInfo(
        id=ID,
        password="wrong_password"
    )

    # when : 로그인 요청
    with pytest.raises(UserError):
        # when : 로그인 요청
        LogInService().log_in_user(session, mockup)

    user_info = UserInfo(id=ID)
    result = AccountRepository.delete_user_account(session, user_info)
    assert result.id == ID


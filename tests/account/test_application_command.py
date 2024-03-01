import pytest
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.infra.database.repository import AccountRepository
from src.account.adapter.rest.request import SignUpUserRequest, LogInUserRequest
from src.account.application.command import AccountCommandUseCase
from src.account.domain.service.sign_up import SignUpService
from src.account.domain.service.log_in import LogInService


# Mock data
ID = "accountservice1@naver.com"
PASSWORD = "test1234"
NAME = "별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def session():
    yield PostgreManager.get_session()


@pytest.fixture
def command():
    yield AccountCommandUseCase(
        AccountRepository,
        SignUpService(),
        LogInService(),
        PostgreManager.get_session()
    )


@pytest.mark.order(1)
def test_can_sign_up_user(command):
    # given : 유효한 계정 정보
    mockup = SignUpUserRequest(
        id=ID,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )

    # when : 회원 가입 요청
    result = command.sign_up_user(mockup)

    # then : 회원 가입 확인
    assert result.id == ID


@pytest.mark.order(2)
def test_can_log_in_user(session, command):
    mockup = LogInUserRequest(
        id=ID,
        password=PASSWORD
    )

    # when : 로그인 요청
    result = command.log_in_user(mockup)

    # then : 로그인 확인
    assert result.id == ID
    assert len(result.token) > 0

    # 계정 삭제
    result = AccountRepository.delete_user_account(session, result)
    assert result.id == ID

import pytest
from src.shared_kernel.infra.database.connection import PostgreManager
from src.account.domain.service.sign_up import SignUpService
from src.account.infra.database.repository import AccountRepository
from src.account.adapter.rest.request import SignUpUserRequest
from src.account.application.command import AccountCommandUseCase

# Mock data
ID = "accountservice1@naver.com"
PASSWORD = "test1234"
NAME = "별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def session():
    yield PostgreManager.get_session()


def test_can_sign_up_user(session):
    # given : 유효한 계정 정보
    mockup = SignUpUserRequest(
        id=ID,
        password=PASSWORD,
        name=NAME,
        gender=GENDER,
        age=AGE
    )

    # when : 회원 가입 요청
    command = AccountCommandUseCase(SignUpService, AccountRepository, session)
    result = command.sign_up_user(mockup)

    # then : 회원 가입 확인
    assert result.id == ID

    # 계정 삭제
    result = AccountRepository.delete_user_account(session, result)
    assert result.id == ID

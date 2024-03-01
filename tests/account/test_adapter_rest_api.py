import pytest
from src.shared_kernel.adapter.app import create_app
from src.account.infra.database.repository import AccountRepository
from src.account.domain.entity import UserInfo
from src.shared_kernel.infra.database.connection import PostgreManager
from fastapi.testclient import TestClient

# Mock data
ID = "h211@naver.com"
PASSWORD = "test1234"
NAME = "별명"
GENDER = "male"
AGE = "20대"


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.fixture
def session():
    yield PostgreManager.get_session()


@pytest.mark.order(1)
def test_can_sign_up_with_valid(client):
    # given : 유효한 payload
    mockup = {
        "id": ID,
        "password": PASSWORD,
        "name": NAME,
        "gender": GENDER,
        "age": AGE
    }

    # when : 회원가입 요청
    response = client.post(
        "/account/signup",
        json=mockup
    )

    # then : 정상 응답
    print(response.json())
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["id"] == ID


# @pytest.mark.order(1)
# def test_cannot_sign_up_with_invalid(client):
#     ## given : 유효하지 않은 payload(name 없이)
#     mockup = {
#         "id": ID,
#         "password": PASSWORD,
#         "gender": GENDER,
#         "age": AGE
#     }

#     # when : 회원가입 요청
#     response = client.post(
#         "/account/signup",
#         json=mockup
#     )

#     # then : 에러 응답(pydantic type error)
#     assert response.status_code == 422
#     assert response.json()["meta"]["message"] == "A required value is missing. Please check."


# @pytest.mark.order(1)
# def test_cannot_log_in_with_invalid(client, session):
#     # given : 유효한 payload
#     mockup = {
#         "id": ID
#     }

#     # when : 로그인 요청
#     response = client.post(
#         "/account/login",
#         json=mockup
#     )

#     # then : 에러 응답(pydantic type error)
#     assert response.status_code == 422
#     assert response.json()["meta"]["message"] == "A required value is missing. Please check."


# @pytest.mark.order(2)
# def test_can_log_in_with_valid(client, session):
#     # given : 유효한 payload
#     mockup = {
#         "id": ID,
#         "password": PASSWORD
#     }

#     # when : 로그인 요청
#     response = client.post(
#         "/account/login",
#         json=mockup
#     )

#     # then : 정상 응답
#     assert response.status_code == 200
#     assert response.json()["meta"]["message"] == "ok"
#     assert response.json()["data"]["id"] == ID
#     assert response.json()["data"]["token"]

#     # 계정 삭제
#     user_info = UserInfo(id=ID)
#     result = AccountRepository.delete_user_account(session, user_info)
#     assert result.id == ID

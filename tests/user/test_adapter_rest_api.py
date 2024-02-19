import os
import pytest
from src.shared_kernel.adapter.app import create_app
from fastapi.testclient import TestClient


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
TOKEN = "mock-token!!!!"
ID = "userservice1@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


def test_user_can_insert_image_with_valid(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN}

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        # when : 이미지 저장 요청
        response = client.post(
            "/user/image",
            headers=headers,
            files=files
        )

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["generated_id"]


def test_user_cannot_insert_image_with_non_header(client):
    # given : 유효하지 않은 payload (header 없이 요청)

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        # when : 이미지 저장 요청
        response = client.post(
            "/user/image",
            files=files
        )

    # then : 422
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."


def test_user_cannot_insert_image_with_non_image(client):
    # given : 유효하지 않은 payload (file 없이 요청)
    headers = {"id": ID, "token": TOKEN}

    # when : 이미지 저장 요청
    response = client.post(
            "/user/image",
            headers=headers
        )
    
    # given : 에러메시지
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."
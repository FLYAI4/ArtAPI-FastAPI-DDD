import os
import pytest
from src.shared_kernel.adapter.app import create_app
from fastapi.testclient import TestClient


user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
TOKEN = "mock-token!!!!"
ID = "kim@naver.com"
IMAGE_PATH = os.path.abspath(os.path.join(test_img_path, "test.jpg"))


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.fixture
def token():
    yield ""

@pytest.mark.asyncio
async def test_user_can_insert_image_with_valid(client, token):
    # given : 유효한 payload
    headers = {"id": ID, "token": token}
    print(headers)

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
    print(response.json()["data"]["generated_id"])


@pytest.mark.asyncio
async def test_user_cannot_insert_image_with_non_header(client):
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


@pytest.mark.asyncio
async def test_user_cannot_insert_image_with_non_image(client, token):
    # given : 유효하지 않은 payload (file 없이 요청)
    headers = {"id": ID, "token": token}

    # when : 이미지 저장 요청
    response = client.post(
            "/user/image",
            headers=headers
        )

    # given : 에러메시지
    assert response.status_code == 422
    assert response.json()["meta"]["message"] == "A required value is missing. Please check."


@pytest.mark.asyncio
async def test_user_can_get_main_content(client, token):
    # given : 유효한 payload
    headers = {"id": ID, "token": token, "generated-id": "4.jpg"}

    # when : 콘텐츠 요청
    response = client.get(
        "/user/content",
        headers=headers
    )

    # given : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["audio_content"]
    assert response.json()["data"]["resize_image"]
    print(response.json()["data"]["text_content"])


@pytest.mark.asyncio
async def test_user_can_get_coord_content(client, token):
    # given : 유효한 payload
    headers = {"id": ID, "token": token, "generated-id": "4.jpg"}

    # when : 콘텐츠 요청
    response = client.get(
        "/user/content/coord",
        headers=headers
    )

    # given : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["coord_content"]


@pytest.mark.asyncio
async def test_user_can_get_video_content(client, token):
    # given : 유효한 payload
    headers = {"id": ID, "token": token, "generated-id": "4.jpg"}

    # when : 콘텐츠 요청
    response = client.get(
        "/user/content/video",
        headers=headers
    )

    # given : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["video_content"]


@pytest.mark.asyncio
async def test_user_can_insert_user_content_review(client, token):
    # given : 유효한 payload
    headers = {"id": ID, "token": token, "generated-id": "4.jpg"}
    body = {"like_status": True, "review_content": "thank you!!"}

    # when : 콘텐츠 요청
    response = client.post(
        "/user/content/review",
        headers=headers,
        json=body
    )

    # given : 정상 응답
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["id"] == ID

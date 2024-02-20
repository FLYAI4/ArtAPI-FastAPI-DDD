import os
import pytest
import httpx
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


# def test_user_can_insert_image_with_valid(client):
#     # given : 유효한 payload
#     headers = {"id": ID, "token": TOKEN}

#     with open(IMAGE_PATH, "rb") as f:
#         files = {"file": ("image.jpg", f, "image/jpeg")}
#         # when : 이미지 저장 요청
#         response = client.post(
#             "/user/image",
#             headers=headers,
#             files=files
#         )

#     # then : 정상 응답 username
#     assert response.status_code == 200
#     assert response.json()["meta"]["message"] == "ok"
#     assert response.json()["data"]["generated_id"]


# def test_user_cannot_insert_image_with_non_header(client):
#     # given : 유효하지 않은 payload (header 없이 요청)

#     with open(IMAGE_PATH, "rb") as f:
#         files = {"file": ("image.jpg", f, "image/jpeg")}
#         # when : 이미지 저장 요청
#         response = client.post(
#             "/user/image",
#             files=files
#         )

#     # then : 422
#     assert response.status_code == 422
#     assert response.json()["meta"]["message"] == "A required value is missing. Please check."


# def test_user_cannot_insert_image_with_non_image(client):
#     # given : 유효하지 않은 payload (file 없이 요청)
#     headers = {"id": ID, "token": TOKEN}

#     # when : 이미지 저장 요청
#     response = client.post(
#             "/user/image",
#             headers=headers
#         )

#     # given : 에러메시지
#     assert response.status_code == 422
#     assert response.json()["meta"]["message"] == "A required value is missing. Please check."


# @pytest.mark.asyncio
# async def test_generate_content(client):
#     headers = {"id": ID, "token": TOKEN}
#     with open(IMAGE_PATH, "rb") as f:
#         files = {"file": ("image.jpg", f, "image/jpeg")}
#         # when : 이미지 저장 요청
#         response = client.post(
#             "/user/image",
#             headers=headers,
#             files=files
#         )

#     # then : 정상 응답 username
#     assert response.status_code == 200
#     assert response.json()["meta"]["message"] == "ok"
#     assert response.json()["data"]["generated_id"]

#     # given : 유효한 payload
#     body = {
#         "generated_id": response.json()["data"]["generated_id"]
#     }

#     # when : 이미지 저장 요청
#     app = create_app()
#     async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac_client:
#         response = await ac_client.post("/user/content",
#                                         headers=headers,
#                                         json=body)
#         assert response.status_code == 200

#         # async for chunk in response.aiter_bytes():
#         #     print(chunk)


def test_user_can_demo_insert_image_with_valid(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN}

    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        # when : 이미지 저장 요청
        response = client.post(
            "/user/image/demo",
            headers=headers,
            files=files
        )

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["generated_id"]


@pytest.mark.asyncio
async def test_demo_generate_content(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN, "generated_id": "demo"}

    # when : 이미지 저장 요청
    app = create_app()
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac_client:
        response = await ac_client.get("/user/content/demo", headers=headers)
        assert response.status_code == 200

        # async for chunk in response.aiter_bytes():
        #     print(chunk)


def test_user_can_demo_get_text_audio_content(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN, "generated_id": "demo"}

    response = client.get(
            "/user/content/text/demo",
            headers=headers
        )

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["text_content"]


def test_user_can_demo_get_coord_content(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN, "generated_id": "demo"}

    response = client.get(
            "/user/content/coord/demo",
            headers=headers
        )

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["나무"]


def test_user_can_demo_get_video_content(client):
    # given : 유효한 payload
    headers = {"id": ID, "token": TOKEN, "generated_id": "demo"}

    response = client.get(
            "/user/content/video/demo",
            headers=headers
        )

    # then : 정상 응답 username
    assert response.status_code == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["video_content"]

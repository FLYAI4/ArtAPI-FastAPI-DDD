import os
import pytest
from fastapi.testclient import TestClient
from src.shared_kernel.adapter.app import create_app
from src.shared_kernel.infra.database.connection import MongoManager
from src.admin.infra.database.repository import AdminRepository
from src.admin.domain.entity import GeneratedContentName

user_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
test_img_path = os.path.abspath(os.path.join(user_path, "test_img"))

# Mock data
IMAGE_NAME = "test.jpg"


@pytest.fixture
def client():
    app = create_app()
    yield TestClient(app)


@pytest.mark.asyncio
async def test_admin_can_generate_content_with_valid(client):
    image_path = os.path.abspath(os.path.join(test_img_path, "origin_img.jpg"))

    with open(image_path, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}

        response = client.post(
            "/admin/content",
            headers={"imagename": IMAGE_NAME},
            files=files,
        )

    assert response.status_code == 200
    print(response.json())
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"]["image_name"]

    # 삭제
    mockup = GeneratedContentName(
        image_name=IMAGE_NAME
    )
    mongo_session = MongoManager.get_session()
    AdminRepository.delete_text_content(mongo_session, mockup)

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Headers

pytestmark = pytest.mark.asyncio

get_and_update_data = [
    {"comment_id": 1, "status_code": 200},
    {"comment_id": 22, "status_code": 404},
]

create_data = [
    {"text": "string", "post_id": 1, "parent_id": 0, "status_code": 200},
    {"text": "string", "post_id": 1, "parent_id": 1, "status_code": 200},
    {"text": "string", "post_id": 22, "parent_id": 1, "status_code": 400},
]

delete_data = [
    {"comment_id": 1, "status_code": 204},
    {"comment_id": 1, "status_code": 404},
    {"comment_id": 33, "status_code": 404},
]


@pytest.mark.parametrize("create_data", create_data)
async def test_create_comment(app: FastAPI, token: str, post_repository, create_data) -> None:
    await post_repository.add_post(author_id=1, title="test", text="test")
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.post(
            "http://test/api/comments",
            json=create_data
        )
    assert response.status_code == create_data["status_code"]


@pytest.mark.parametrize("get_data", get_and_update_data)
async def test_get_comment(app: FastAPI, token: str, post_repository, get_data) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.get(f"http://test/api/comments/{get_data['comment_id']}")
    assert response.status_code == get_data["status_code"]


@pytest.mark.parametrize("update_data", get_and_update_data)
async def test_update_comment(app: FastAPI, token: str, post_repository, update_data) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.patch(
            f"http://test/api/comments/{update_data['comment_id']}",
            json={"text": "testww"}
        )
    assert response.status_code == update_data["status_code"]


@pytest.mark.parametrize("delete_data", delete_data)
async def test_delete_comment(app: FastAPI, token: str, post_repository, delete_data) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.delete(
            f"http://test/api/comments/{delete_data['comment_id']}",
        )
    assert response.status_code == delete_data["status_code"]
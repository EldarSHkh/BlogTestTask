import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Headers

pytestmark = pytest.mark.asyncio


get_and_update_data = [
    {"post_id": 1, "status_code": 200},
    {"post_id": 2, "status_code": 404},
]

delete_response = [
    {"status_code": 204},
    {"status_code": 404},
]


async def test_create_post(app: FastAPI, token: str) -> None:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=Headers({"Authorization": f"Bearer {token}"}),
    ) as client:
        response = await client.post(
            "http://test/api/posts", json={"title": "string", "text": "string"}
        )
    assert response.status_code == 200


@pytest.mark.parametrize("update_data", get_and_update_data)
async def test_update_post(app: FastAPI, token: str, update_data) -> None:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=Headers({"Authorization": f"Bearer {token}"}),
    ) as client:
        response = await client.patch(
            f"http://test/api/posts/{update_data['post_id']}",
            json={"title": "qwerty", "text": "qwerty"},
        )
    assert response.status_code == update_data["status_code"]
    if update_data["status_code"] == 200:
        assert response.json()["title"] == "qwerty"
        assert response.json()["text"] == "qwerty"


@pytest.mark.parametrize("get_data", get_and_update_data)
async def test_get_post(app: FastAPI, token: str, get_data) -> None:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=Headers({"Authorization": f"Bearer {token}"}),
    ) as client:
        response = await client.get(f"http://test/api/posts/{get_data['post_id']}")
    assert response.status_code == get_data["status_code"]


@pytest.mark.parametrize("delete_response", delete_response)
async def test_delete_post(app: FastAPI, token: str, delete_response) -> None:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=Headers({"Authorization": f"Bearer {token}"}),
    ) as client:
        response = await client.delete("http://test/api/posts/1")
    assert response.status_code == delete_response["status_code"]

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Headers

pytestmark = pytest.mark.asyncio


get_data = [
    {"user_id": 1, "status_code": 200},
    {"user_id": 2, "status_code": 404},
]

delete_response = [
    {"status_code": 204},
    {"status_code": 404},
]


@pytest.mark.parametrize("get_data", get_data)
async def test_get_user(app: FastAPI, token: str, get_data) -> None:

    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.get(f"http://test/api/users/{get_data['user_id']}")
    assert response.status_code == get_data['status_code']


async def test_update_user(app: FastAPI, token) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.put(
            "http://test/api/users/password",
            json={
                "new_password": "qwerty",
                "current_password": "string"
            }
        )
    assert response.status_code == 200


@pytest.mark.parametrize("delete_response", delete_response)
async def test_delete_user(app: FastAPI, token: str, delete_response) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
            headers=Headers({"Authorization": f"Bearer {token}"})
    ) as client:
        response = await client.delete(
            f"http://test/api/users/1"
        )
    assert response.status_code == delete_response["status_code"]

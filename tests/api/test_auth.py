import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


data_register = [
    {"login": "string", "password": "string", "status_code": 201},
    {"login": "string", "password": "string", "status_code": 400},
]


@pytest.mark.parametrize("data_register", data_register)
async def test_registration(app: FastAPI,  data_register) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
    ) as client:
        response = await client.post("http://test/api/auth/register", json=data_register)
    assert response.status_code == data_register["status_code"]


data_login = [
    {"login": "string", "password": "string", "status_code": 200},
    {"login": "qwerty", "password": "qwerty", "status_code": 401},
]


@pytest.mark.parametrize("data_login", data_login)
async def test_login(app: FastAPI, data_login) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
    ) as client:
        response = await client.post("http://test/api/auth/login", json=data_login)
    assert response.status_code == data_login["status_code"]

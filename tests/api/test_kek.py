import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_kek(app: FastAPI) -> None:
    async with AsyncClient(
            app=app,
            base_url="http://test",
    ) as client:
        response = await client.get("http://test/api/test")
    assert response.status_code == 200
    assert response.json() == {"test": "test"}


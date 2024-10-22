import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_e2_create_user(
    client: AsyncClient,
):
    payload = {
        "name": "Jhon Doe",
        "email": "jhondoe@example.com",
        "password": "ABC123456",
    }

    response = await client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_e2e_create_user_with_same_email_twice(
    client: AsyncClient,
):
    payload = {
        "name": "Jhon Doe",
        "email": "jhondoe@example.com",
        "password": "ABC123456",
    }

    await client.post("/api/v1/users/", json=payload)

    response = await client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400

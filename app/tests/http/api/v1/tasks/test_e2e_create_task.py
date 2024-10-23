from datetime import timedelta, datetime

import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient

from app.domain.entities.category import Category
from app.domain.entities.user import User

faker = Faker()


@pytest_asyncio.fixture
async def payload(
    category: Category,
):
    payload = {
        "title": faker.text(max_nb_chars=30),
        "description": faker.text(max_nb_chars=100),
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(timespec="seconds"),
        "priority": "low",
        "category_id": category.id.__str__(),
    }
    return payload


@pytest.mark.asyncio
async def test_e2e_create_task(
    client: AsyncClient, payload: dict, bearer_token: str, user: User
):
    response = await client.post(
        "/api/v1/tasks/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["category_id"] == payload["category_id"]
    assert data["user_id"] == user.id.__str__()


@pytest.mark.asyncio
async def test_e2e_create_task_without_token(
    client: AsyncClient, payload: dict, user: User
):
    response = await client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_create_task_without_title(
    client: AsyncClient, payload: dict, bearer_token: str, user: User
):
    payload["title"] = None
    response = await client.post(
        "/api/v1/tasks/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_e2e_create_task_with_invalid_title(
    client: AsyncClient, payload: dict, bearer_token: str, user: User
):
    payload["title"] = "A" * 101
    response = await client.post(
        "/api/v1/tasks/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_e2e_create_task_with_invalid_due_date(
    client: AsyncClient, payload: dict, bearer_token: str, user: User
):
    payload["due_date"] = datetime.now().isoformat(timespec="seconds")
    response = await client.post(
        "/api/v1/tasks/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 422

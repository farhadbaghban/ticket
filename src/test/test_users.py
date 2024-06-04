import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient, user_payload: dict):
    response = await async_client.post("/users/", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_read_users(async_client: AsyncClient):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_read_user(async_client: AsyncClient, user_payload: dict):
    # First, create a user
    await async_client.post("/users/", json=user_payload)

    # Then, read the user
    response = await async_client.get(f"/users/{user_payload['email']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient, user_payload: dict):
    # First, create a user
    await async_client.post("/users/", json=user_payload)

    # Then, delete the user
    response = await async_client.delete("/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient, user_payload: dict):
    # First, create a user
    await async_client.post("/users/", json=user_payload)

    # Then, login with the user credentials
    response = await async_client.post("/users/login", json=user_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

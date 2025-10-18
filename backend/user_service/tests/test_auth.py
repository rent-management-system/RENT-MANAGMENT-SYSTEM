import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register a new user
    response = await client.post(
        "/api/v1/users/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@example.com"

    # Login with the new user
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_change_password(client: AsyncClient):
    # Register and login
    await client.post("/api/v1/users/register", json={"email": "test2@example.com", "password": "oldpassword", "full_name": "Test User 2"})
    login_response = await client.post("/api/v1/auth/login", data={"username": "test2@example.com", "password": "oldpassword"}, headers={"content-type": "application/x-www-form-urlencoded"})
    access_token = login_response.json()["access_token"]

    # Change password
    response = await client.post(
        "/api/v1/auth/change-password",
        json={"old_password": "oldpassword", "new_password": "newpassword"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    # Login with the new password
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test2@example.com", "password": "newpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200

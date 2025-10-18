import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_update_me(client: AsyncClient):
    # Register and login
    await client.post("/api/v1/users/register", json={"email": "test3@example.com", "password": "testpassword", "full_name": "Test User 3"})
    login_response = await client.post("/api/v1/auth/login", data={"username": "test3@example.com", "password": "testpassword"}, headers={"content-type": "application/x-www-form-urlencoded"})
    access_token = login_response.json()["access_token"]

    # Get user profile
    response = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test3@example.com"
    assert user["full_name"] == "Test User 3"

    # Update user profile
    response = await client.put(
        "/api/v1/users/me",
        json={"full_name": "Updated Test User 3"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["full_name"] == "Updated Test User 3"

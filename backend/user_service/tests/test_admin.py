import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_users_as_admin(client: AsyncClient):
    # Login as admin
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin_test@example.com", "password": "adminpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    access_token = login_response.json()["access_token"]

    # Get all users
    response = await client.get("/api/v1/admin/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0

@pytest.mark.asyncio
async def test_read_user_as_admin(client: AsyncClient):
    # Register a new user to be fetched
    register_response = await client.post(
        "/api/v1/users/register",
        json={
            "email": "test_to_fetch@example.com",
            "password": "testpassword",
            "full_name": "Test To Fetch",
        },
    )
    user_to_fetch_id = register_response.json()["id"]

    # Login as admin
    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin_test@example.com", "password": "adminpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    access_token = login_response.json()["access_token"]

    # Get the user by ID
    response = await client.get(f"/api/v1/admin/users/{user_to_fetch_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test_to_fetch@example.com"

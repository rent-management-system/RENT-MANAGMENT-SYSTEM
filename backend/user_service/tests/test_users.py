import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole, Language, Currency
from app.schemas.user import UserCreate
from app.crud import create_user
from app.core.security import encrypt_data, decrypt_data

@pytest.fixture
async def authenticated_user_client(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="authenticated@example.com",
        password="securepassword",
        full_name="Authenticated User",
        phone_number="+251911000001",
        preferred_language=Language.EN,
        preferred_currency=Currency.ETB,
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "authenticated@example.com",
            "password": "securepassword"
        }
    )
    access_token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client

@pytest.mark.asyncio
async def test_read_users_me(authenticated_user_client: AsyncClient):
    response = await authenticated_user_client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == "authenticated@example.com"
    assert response.json()["full_name"] == "Authenticated User"
    assert response.json()["phone_number"] == "+251911000001"

@pytest.mark.asyncio
async def test_update_user_me(authenticated_user_client: AsyncClient, test_db: AsyncSession):
    update_data = {
        "full_name": "Updated User Name",
        "phone_number": "+251911000002",
        "preferred_language": "am",
        "preferred_currency": "USD"
    }
    response = await authenticated_user_client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated User Name"
    assert response.json()["phone_number"] == "+251911000002"
    assert response.json()["preferred_language"] == "am"
    assert response.json()["preferred_currency"] == "USD"

    # Verify in DB that phone number is encrypted
    user_in_db = await test_db.get(User, response.json()["id"])
    assert user_in_db.phone_number != update_data["phone_number"].encode()
    assert decrypt_data(user_in_db.phone_number) == update_data["phone_number"]

@pytest.mark.asyncio
async def test_update_user_me_invalid_phone_number(authenticated_user_client: AsyncClient):
    update_data = {
        "phone_number": "invalid-phone"
    }
    response = await authenticated_user_client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

@pytest.mark.asyncio
async def test_update_user_me_partial_update(authenticated_user_client: AsyncClient):
    update_data = {
        "full_name": "Partial Update"
    }
    response = await authenticated_user_client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Partial Update"
    # Other fields should remain unchanged from fixture
    assert response.json()["phone_number"] == "+251911000001"
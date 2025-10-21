import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.crud import create_user

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, test_db: AsyncSession):
    user_data = {
        "email": "test@example.com",
        "password": "securepassword",
        "full_name": "Test User",
        "phone_number": "+251911223344",
        "preferred_language": "en",
        "preferred_currency": "ETB"
    }
    response = await client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["full_name"] == "Test User"
    assert response.json()["role"] == "tenant"
    assert response.json()["phone_number"] == "+251911223344"

@pytest.mark.asyncio
async def test_register_admin_forbidden(client: AsyncClient, test_db: AsyncSession):
    admin_data = {
        "email": "admin_reg@example.com",
        "password": "securepassword",
        "full_name": "Admin Register",
        "role": "admin"
    }
    response = await client.post("/api/v1/users/register", json=admin_data)
    assert response.status_code == 403
    assert "Cannot register as an admin." in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="login@example.com",
        password="loginpassword",
        full_name="Login User",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "loginpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_login_incorrect_password(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="wrongpass@example.com",
        password="correctpassword",
        full_name="Wrong Pass User",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "incorrectpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="inactive@example.com",
        password="activepassword",
        full_name="Inactive User",
        role=UserRole.TENANT
    )
    user = await create_user(test_db, user=user_data)
    user.is_active = False
    test_db.add(user)
    await test_db.commit()

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "inactive@example.com",
            "password": "activepassword"
        }
    )
    assert response.status_code == 400
    assert "Inactive user" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_preseeded_admin_force_password_change(client: AsyncClient, test_db: AsyncSession):
    # Manually create a pre-seeded admin with password_changed=False
    admin_email = settings.DEFAULT_ADMIN_EMAIL
    admin_password = settings.DEFAULT_ADMIN_PASSWORD
    hashed_password = get_password_hash(admin_password)
    admin_user = User(
        email=admin_email,
        password=hashed_password,
        full_name="Preseeded Admin",
        role=UserRole.ADMIN,
        password_changed=False
    )
    test_db.add(admin_user)
    await test_db.commit()

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": admin_email,
            "password": admin_password
        }
    )
    assert response.status_code == 403
    assert "Please change your password on first login." in response.json()["detail"]

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="refresh@example.com",
        password="refreshpassword",
        full_name="Refresh User",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "refresh@example.com",
            "password": "refreshpassword"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()
    assert "refresh_token" in refresh_response.json()

@pytest.mark.asyncio
async def test_change_password_success(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="changepass@example.com",
        password="oldpassword",
        full_name="Change Pass User",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "changepass@example.com",
            "password": "oldpassword"
        }
    )
    access_token = login_response.json()["access_token"]

    change_password_response = await client.post(
        "/api/v1/auth/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "old_password": "oldpassword",
            "new_password": "newsecurepassword"
        }
    )
    assert change_password_response.status_code == 200
    assert "Password changed successfully" in change_password_response.json()["message"]

    # Try logging in with new password
    new_login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "changepass@example.com",
            "password": "newsecurepassword"
        }
    )
    assert new_login_response.status_code == 200

@pytest.mark.asyncio
async def test_verify_token_success(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="verify@example.com",
        password="verifypassword",
        full_name="Verify User",
        phone_number="+251911000000",
        preferred_language="am",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "verify@example.com",
            "password": "verifypassword"
        }
    )
    access_token = login_response.json()["access_token"]

    verify_response = await client.get(
        "/api/v1/auth/verify",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["email"] == "verify@example.com"
    assert verify_response.json()["role"] == "tenant"
    assert verify_response.json()["phone_number"] == "+251911000000"
    assert verify_response.json()["preferred_language"] == "am"
    assert "user_id" in verify_response.json()

@pytest.mark.asyncio
async def test_verify_token_invalid(client: AsyncClient):
    response = await client.get(
        "/api/v1/auth/verify",
        headers={
            "Authorization": "Bearer invalidtoken"
        }
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]
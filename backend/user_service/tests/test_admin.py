import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole, Language, Currency
from app.schemas.user import UserCreate
from app.crud import create_user
from app.core.config import settings
from app.core.security import get_password_hash

@pytest.fixture
async def admin_authenticated_client(client: AsyncClient, test_db: AsyncSession):
    admin_email = settings.DEFAULT_ADMIN_EMAIL
    admin_password = settings.DEFAULT_ADMIN_PASSWORD
    hashed_password = get_password_hash(admin_password)
    admin_user = User(
        email=admin_email,
        password=hashed_password,
        full_name="Admin User",
        role=UserRole.ADMIN,
        password_changed=True # Assume password is changed for testing admin endpoints
    )
    test_db.add(admin_user)
    await test_db.commit()

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": admin_email,
            "password": admin_password
        }
    )
    access_token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client

@pytest.fixture
async def tenant_authenticated_client(client: AsyncClient, test_db: AsyncSession):
    user_data = UserCreate(
        email="tenant_admin_test@example.com",
        password="securepassword",
        full_name="Tenant User",
        role=UserRole.TENANT
    )
    await create_user(test_db, user=user_data)

    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "tenant_admin_test@example.com",
            "password": "securepassword"
        }
    )
    access_token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client

@pytest.mark.asyncio
async def test_admin_list_users_success(admin_authenticated_client: AsyncClient, test_db: AsyncSession):
    # Create some test users
    user1 = UserCreate(email="user1@example.com", password="pass1", full_name="User One", role=UserRole.TENANT)
    user2 = UserCreate(email="user2@example.com", password="pass2", full_name="User Two", role=UserRole.OWNER)
    await create_user(test_db, user=user1)
    await create_user(test_db, user=user2)

    response = await admin_authenticated_client.get("/api/v1/admin/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 3 # Includes the seeded admin and the two created users
    assert any(u["email"] == "user1@example.com" for u in users)
    assert any(u["email"] == "user2@example.com" for u in users)

@pytest.mark.asyncio
async def test_admin_list_users_forbidden_for_tenant(tenant_authenticated_client: AsyncClient):
    response = await tenant_authenticated_client.get("/api/v1/admin/users")
    assert response.status_code == 403
    assert "The user does not have enough privileges" in response.json()["detail"]

@pytest.mark.asyncio
async def test_admin_get_user_by_id_success(admin_authenticated_client: AsyncClient, test_db: AsyncSession):
    user_to_get = UserCreate(email="getbyid@example.com", password="getpass", full_name="Get By ID User", role=UserRole.BROKER)
    created_user = await create_user(test_db, user=user_to_get)

    response = await admin_authenticated_client.get(f"/api/v1/admin/users/{created_user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "getbyid@example.com"
    assert response.json()["full_name"] == "Get By ID User"

@pytest.mark.asyncio
async def test_admin_get_user_by_id_not_found(admin_authenticated_client: AsyncClient):
    non_existent_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" # A random UUID
    response = await admin_authenticated_client.get(f"/api/v1/admin/users/{non_existent_id}")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_admin_get_user_by_id_forbidden_for_tenant(tenant_authenticated_client: AsyncClient):
    some_user_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" # Doesn't matter if it exists, permission denied first
    response = await tenant_authenticated_client.get(f"/api/v1/admin/users/{some_user_id}")
    assert response.status_code == 403
    assert "The user does not have enough privileges" in response.json()["detail"]
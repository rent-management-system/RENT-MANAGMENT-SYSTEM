import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import pytz

from app.models.user import RefreshToken, User, UserRole
from app.crud import create_user, create_refresh_token_db
from app.utils.cleanup import cleanup_expired_refresh_tokens
from app.core.config import settings
from app.core.security import get_password_hash

@pytest.fixture
async def setup_refresh_tokens(test_db: AsyncSession):
    # Create a user
    user_data = {
        "email": "cleanup_user@example.com",
        "password": "securepassword",
        "full_name": "Cleanup User",
        "role": UserRole.TENANT
    }
    user = await create_user(test_db, user=user_data)

    # Create an expired refresh token
    expired_token_raw = "expired_token_hash"
    expired_token_hashed = get_password_hash(expired_token_raw)
    expired_at = datetime.utcnow() - timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS + 1)
    await create_refresh_token_db(test_db, user.id, expired_token_hashed, expired_at)

    # Create a valid refresh token
    valid_token_raw = "valid_token_hash"
    valid_token_hashed = get_password_hash(valid_token_raw)
    valid_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS - 1)
    await create_refresh_token_db(test_db, user.id, valid_token_hashed, valid_at)

    return user

@pytest.mark.asyncio
async def test_cleanup_expired_refresh_tokens(test_db: AsyncSession, setup_refresh_tokens):
    # Ensure there are expired and valid tokens before cleanup
    initial_tokens = (await test_db.execute(select(RefreshToken))).scalars().all()
    assert len(initial_tokens) == 2

    # Run the cleanup job
    await cleanup_expired_refresh_tokens()

    # Check if expired token is deleted and valid token remains
    remaining_tokens = (await test_db.execute(select(RefreshToken))).scalars().all()
    assert len(remaining_tokens) == 1
    assert remaining_tokens[0].token == get_password_hash("valid_token_hash")

@pytest.mark.asyncio
async def test_cleanup_no_expired_tokens(test_db: AsyncSession):
    # Create a user
    user_data = {
        "email": "no_expired@example.com",
        "password": "securepassword",
        "full_name": "No Expired User",
        "role": UserRole.TENANT
    }
    user = await create_user(test_db, user=user_data)

    # Create only valid refresh tokens
    valid_token_raw = "another_valid_token_hash"
    valid_token_hashed = get_password_hash(valid_token_raw)
    valid_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS - 1)
    await create_refresh_token_db(test_db, user.id, valid_token_hashed, valid_at)

    initial_tokens = (await test_db.execute(select(RefreshToken))).scalars().all()
    assert len(initial_tokens) == 1

    # Run the cleanup job
    await cleanup_expired_refresh_tokens()

    # No tokens should be deleted
    remaining_tokens = (await test_db.execute(select(RefreshToken))).scalars().all()
    assert len(remaining_tokens) == 1
    assert remaining_tokens[0].token == get_password_hash("another_valid_token_hash")

# Mocking database failure for error handling test
class MockAsyncSession:
    async def execute(self, statement):
        if isinstance(statement, Delete):
            raise Exception("Simulated DB error during cleanup")
        return MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[]))))

    async def commit(self):
        pass

    async def rollback(self):
        pass

@pytest.mark.asyncio
async def test_cleanup_error_handling(monkeypatch):
    # Mock get_db to return our mock session
    async def mock_get_db():
        yield MockAsyncSession()
    
    monkeypatch.setattr("app.utils.cleanup.get_db", mock_get_db)

    with pytest.raises(Exception, match="Simulated DB error during cleanup"):
        await cleanup_expired_refresh_tokens()

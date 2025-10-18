import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.models.user import Base, User, UserRole
from app.core.security import get_password_hash

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed an admin user
    async with TestingSessionLocal() as session:
        admin_user = User(
            email="admin_test@example.com",
            password=get_password_hash("adminpassword"),
            full_name="Admin Test User",
            role=UserRole.ADMIN,
        )
        session.add(admin_user)
        await session.commit()

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

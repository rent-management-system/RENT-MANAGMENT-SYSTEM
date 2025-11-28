from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from ..core.config import settings

# Configure connection pool settings for Supabase free tier
# Free tier typically allows 1-2 concurrent connections
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=2,  # Very conservative pool size for free tier
    max_overflow=1,  # Allow 1 additional connection beyond pool_size
    pool_timeout=10,  # Shorter timeout to fail fast
    pool_recycle=300,  # Recycle connections more frequently (5 minutes)
    pool_pre_ping=True,  # Check connections before using them
    pool_use_lifo=True,  # Better connection reuse
    connect_args={
        'server_settings': {
            'application_name': 'rental_app',
            'statement_timeout': '10000'  # 10 second statement timeout
        }
    }
)

from typing import AsyncGenerator
from contextlib import asynccontextmanager

async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session."""
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
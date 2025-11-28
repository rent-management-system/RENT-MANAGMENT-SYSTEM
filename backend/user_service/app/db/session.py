from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from ..core.config import settings

# Configure connection settings for Supabase free tier
# Using NullPool to avoid connection pool issues with free tier
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    poolclass=NullPool,  # Don't use connection pooling with free tier
    connect_args={
        'server_settings': {
            'application_name': 'rental_app',
            'statement_timeout': '5000',  # 5 second statement timeout
            'idle_in_transaction_session_timeout': '10000'  # 10 second idle timeout
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
    session = None
    try:
        session = async_session()
        yield session
    except Exception as e:
        if session:
            await session.rollback()
        raise e
    finally:
        if session:
            await session.close()
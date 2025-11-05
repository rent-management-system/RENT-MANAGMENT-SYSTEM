from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=30,  # Adjust as needed
    max_overflow=50, # Adjust as needed
)

from typing import AsyncGenerator
from contextlib import asynccontextmanager

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
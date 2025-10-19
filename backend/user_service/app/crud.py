from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from .models.user import User, RefreshToken
from .schemas.user import UserCreate
from .core.security import get_password_hash, encrypt_data, decrypt_data
from .utils.retry import async_retry
import uuid
from datetime import datetime

@async_retry()
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user and user.phone_number:
        user.phone_number = decrypt_data(user.phone_number) # Decrypt for use
    return user

@async_retry()
async def get_user(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    user = await db.get(User, user_id)
    if user and user.phone_number:
        user.phone_number = decrypt_data(user.phone_number) # Decrypt for use
    return user

@async_retry()
async def create_user(db: AsyncSession, user: UserCreate, password_changed: bool = True) -> User:
    hashed_password = get_password_hash(user.password)
    encrypted_phone_number = encrypt_data(user.phone_number) if user.phone_number else None
    db_user = User(
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        phone_number=encrypted_phone_number,
        preferred_language=user.preferred_language,
        preferred_currency=user.preferred_currency,
        password_changed=password_changed # Set password_changed status
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    # Decrypt phone number before returning
    if db_user.phone_number:
        db_user.phone_number = decrypt_data(db_user.phone_number)
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    for user in users:
        if user.phone_number:
            user.phone_number = decrypt_data(user.phone_number)
    return users

@async_retry()
async def create_refresh_token_db(db: AsyncSession, user_id: uuid.UUID, token: str, expires_at: datetime) -> RefreshToken:
    db_refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_refresh_token)
    await db.commit()
    await db.refresh(db_refresh_token)
    return db_refresh_token

@async_retry()
async def get_refresh_token_by_token(db: AsyncSession, token: str) -> RefreshToken | None:
    result = await db.execute(select(RefreshToken).filter(RefreshToken.token == token))
    return result.scalars().first()

@async_retry()
async def delete_refresh_token(db: AsyncSession, refresh_token_id: uuid.UUID):
    await db.execute(delete(RefreshToken).where(RefreshToken.id == refresh_token_id))
    await db.commit()
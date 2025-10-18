from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, encrypt_data
import uuid

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, user: UserCreate) -> User:
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
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
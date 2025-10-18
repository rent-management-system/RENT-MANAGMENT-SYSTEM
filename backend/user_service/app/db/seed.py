from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.models.user import UserRole

async def seed_admin(db: AsyncSession):
    admin_email = settings.DEFAULT_ADMIN_EMAIL
    admin_password = settings.DEFAULT_ADMIN_PASSWORD

    user = await get_user_by_email(db, email=admin_email)
    if not user:
        admin_user = UserCreate(
            email=admin_email,
            password=admin_password,
            full_name="Admin User",
            role=UserRole.ADMIN,
        )
        await create_user(db, user=admin_user)

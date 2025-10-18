from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.models.user import UserRole

async def seed_admin(db: AsyncSession):
    admin_users_to_seed = [
        {
            "email": settings.DEFAULT_ADMIN_EMAIL,
            "password": settings.DEFAULT_ADMIN_PASSWORD,
            "full_name": "Admin User 1",
        }
    ]

    if settings.DEFAULT_ADMIN_EMAIL_2 and settings.DEFAULT_ADMIN_PASSWORD_2:
        admin_users_to_seed.append(
            {
                "email": settings.DEFAULT_ADMIN_EMAIL_2,
                "password": settings.DEFAULT_ADMIN_PASSWORD_2,
                "full_name": "Admin User 2",
            }
        )

    for admin_data in admin_users_to_seed:
        user = await get_user_by_email(db, email=admin_data["email"])
        if not user:
            admin_user_create = UserCreate(
                email=admin_data["email"],
                password=admin_data["password"],
                full_name=admin_data["full_name"],
                role=UserRole.ADMIN,
            )
            # Set password_changed to False for pre-seeded admins
            await create_user(db, user=admin_user_create, password_changed=False)
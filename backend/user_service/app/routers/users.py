from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies.auth import get_current_user
from ..schemas.user import User, UserCreate, UserUpdate
from ..db.session import get_db
from ..crud import create_user, get_user_by_email
from ..models.user import UserRole
from ..core.security import encrypt_data

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot register as an admin.")

    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db=db, user=user)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(user_in: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_in.full_name:
        current_user.full_name = user_in.full_name
    if user_in.phone_number:
        # The phone_number from user_in is already validated by Pydantic regex
        current_user.phone_number = encrypt_data(user_in.phone_number)
    if user_in.preferred_language:
        current_user.preferred_language = user_in.preferred_language
    if user_in.preferred_currency:
        current_user.preferred_currency = user_in.preferred_currency
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    # Decrypt phone number before returning
    if current_user.phone_number:
        current_user.phone_number = decrypt_data(current_user.phone_number)
    return current_user

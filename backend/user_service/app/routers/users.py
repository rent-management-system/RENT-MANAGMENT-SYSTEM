from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.db.session import get_db
from app.crud import create_user, get_user_by_email

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
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
        # In a real app, you'd want to handle phone number updates carefully
        # e.g., re-verification
        from app.core.security import encrypt_data
        current_user.phone_number = encrypt_data(user_in.phone_number)
    if user_in.preferred_language:
        current_user.preferred_language = user_in.preferred_language
    if user_in.preferred_currency:
        current_user.preferred_currency = user_in.preferred_currency
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

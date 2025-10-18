from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from ..dependencies.auth import require_role
from ..schemas.user import User
from ..db.session import get_db
from ..crud import get_user
from ..models.user import UserRole
from sqlalchemy.future import select
from ..models.user import User as UserModel

router = APIRouter()

@router.get("/users", response_model=List[User], dependencies=[Depends(require_role(UserRole.ADMIN))])
async def read_users(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=User, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def read_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
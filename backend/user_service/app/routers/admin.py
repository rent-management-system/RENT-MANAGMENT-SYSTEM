from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from ..dependencies.auth import get_current_user, require_role
from ..schemas.user import User
from ..db.session import get_db
from ..crud import get_user, get_users
from ..models.user import UserRole

router = APIRouter()

@router.get("/users", response_model=List[User])
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    users = await get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user_by_id(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import User as UserSchema
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
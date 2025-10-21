from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.security import decode_token, decrypt_data
from ..db.session import get_db
from ..models.user import User, UserRole
from ..schemas.token import UserTokenData
from ..crud import get_user
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await get_user(db, user_id) # Use crud function to get user and decrypt phone_number
    if user is None:
        raise credentials_exception
    
    # Ensure the user object returned has all necessary fields for downstream use
    # The crud.get_user already decrypts phone_number
    return user

def require_role(required_roles: List[UserRole]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have enough privileges",
            )
        return current_user
    return role_checker

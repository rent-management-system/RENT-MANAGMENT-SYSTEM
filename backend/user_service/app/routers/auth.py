from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies.auth import get_current_user
from ..schemas.token import Token, RefreshToken
from ..schemas.user import ChangePassword, User
from ..core.security import create_access_token, create_refresh_token, verify_password, get_password_hash, decode_token
from ..db.session import get_db
from ..crud import get_user_by_email, get_user

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value, "email": user.email})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh(db: AsyncSession = Depends(get_db), refresh_token: RefreshToken = Depends()):
    payload = decode_token(refresh_token.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value, "email": user.email})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(db: AsyncSession = Depends(get_db), passwords: ChangePassword = Depends(), current_user: User = Depends(get_current_user)):
    if not verify_password(passwords.old_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")
    
    current_user.password = get_password_hash(passwords.new_password)
    current_user.password_changed = True
    await db.commit()

    return {"message": "Password changed successfully"}

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    return current_user
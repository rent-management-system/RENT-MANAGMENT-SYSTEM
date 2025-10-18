from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies.auth import get_current_user
from ..schemas.token import Token, RefreshToken, UserTokenData
from ..schemas.user import ChangePassword, User
from ..core.security import create_access_token, create_refresh_token, verify_password, get_password_hash, decode_token
from ..db.session import get_db
from ..crud import get_user_by_email, get_user, create_refresh_token_db, get_refresh_token_by_token, delete_refresh_token
from ..models.user import UserRole
from ..core.config import settings
from datetime import datetime, timedelta

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

    # Check if password needs to be changed for pre-seeded admins
    if user.role == UserRole.ADMIN and not user.password_changed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please change your password on first login."
        )

    access_token_data = {
        "sub": str(user.id),
        "role": user.role.value,
        "email": user.email,
        "phone_number": user.phone_number, # Already decrypted by crud.get_user_by_email
        "preferred_language": user.preferred_language.value
    }
    access_token = create_access_token(data=access_token_data)
    
    # Create refresh token and store in DB
    refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    raw_refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    hashed_refresh_token = get_password_hash(raw_refresh_token) # Hash the refresh token before storing
    await create_refresh_token_db(db, user_id=user.id, token=hashed_refresh_token, expires_at=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": raw_refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh(db: AsyncSession = Depends(get_db), refresh_token_obj: RefreshToken = Depends()):
    # Validate the provided refresh token against the database
    db_refresh_token = await get_refresh_token_by_token(db, get_password_hash(refresh_token_obj.refresh_token)) # Compare hashed tokens
    
    if not db_refresh_token or db_refresh_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    
    # Decode the payload from the raw refresh token (not the hashed one from DB)
    payload = decode_token(refresh_token_obj.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")
    
    user_id = payload.get("sub")
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Delete the old refresh token from the database
    await delete_refresh_token(db, db_refresh_token.id)

    access_token_data = {
        "sub": str(user.id),
        "role": user.role.value,
        "email": user.email,
        "phone_number": user.phone_number, # Already decrypted by crud.get_user
        "preferred_language": user.preferred_language.value
    }
    access_token = create_access_token(data=access_token_data)
    
    # Create and store a new refresh token
    new_refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_raw_refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    new_hashed_refresh_token = get_password_hash(new_raw_refresh_token)
    await create_refresh_token_db(db, user_id=user.id, token=new_hashed_refresh_token, expires_at=new_refresh_token_expires)

    return {"access_token": access_token, "refresh_token": new_raw_refresh_token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(db: AsyncSession = Depends(get_db), passwords: ChangePassword = Depends(), current_user: User = Depends(get_current_user)):
    if not verify_password(passwords.old_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")
    
    current_user.password = get_password_hash(passwords.new_password)
    current_user.password_changed = True
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Password changed successfully"}

@router.get("/verify", response_model=UserTokenData)
async def verify_token(current_user: User = Depends(get_current_user)):
    return UserTokenData(
        user_id=current_user.id,
        role=current_user.role,
        email=current_user.email,
        phone_number=current_user.phone_number, # Already decrypted
        preferred_language=current_user.preferred_language
    )
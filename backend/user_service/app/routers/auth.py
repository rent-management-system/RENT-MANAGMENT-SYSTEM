from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import secrets
from pydantic import BaseModel, EmailStr

from ..dependencies.auth import get_current_user
from ..schemas.token import Token, RefreshToken, UserTokenData
from ..schemas.user import ChangePassword, User
from ..core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    decode_token
)
from ..db.session import get_db
from ..crud import (
    get_user_by_email,
    get_user,
    create_refresh_token_db,
    get_refresh_token_by_token,
    delete_refresh_token
)
from ..models.user import UserRole
from ..core.config import settings

from app.utils.send_email import send_reset_email
from app.utils.supabase_client import supabase


router = APIRouter()


# ============================================================
# LOGIN
# ============================================================
@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # if user.role == UserRole.ADMIN and not user.password_changed:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Please change your password on first login."
    #     )

    phone_number_str = (
        user.phone_number.decode("utf-8")
        if isinstance(user.phone_number, bytes)
        else user.phone_number
    )

    access_token_data = {
        "sub": str(user.id),
        "role": user.role.value,
        "email": user.email,
        "phone_number": phone_number_str,
        "preferred_language": user.preferred_language.value
    }

    access_token = create_access_token(data=access_token_data)

    # Create refresh token
    refresh_exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    raw_refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    hashed_refresh_token = get_password_hash(raw_refresh_token)

    await create_refresh_token_db(
        db,
        user_id=user.id,
        token=hashed_refresh_token,
        expires_at=refresh_exp
    )

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "token_type": "bearer"
    }


# ============================================================
# REFRESH TOKEN
# ============================================================
@router.post("/refresh", response_model=Token)
async def refresh(
    db: AsyncSession = Depends(get_db),
    refresh_token_obj: RefreshToken = Depends()
):
    hashed = get_password_hash(refresh_token_obj.refresh_token)
    db_refresh_token = await get_refresh_token_by_token(db, hashed)

    if not db_refresh_token or db_refresh_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    payload = decode_token(refresh_token_obj.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )

    user = await get_user(db, payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Delete old token
    await delete_refresh_token(db, db_refresh_token.id)

    # Create new refresh token
    new_exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_raw = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    new_hashed = get_password_hash(new_raw)

    await create_refresh_token_db(
        db, user_id=user.id, token=new_hashed, expires_at=new_exp
    )

    phone_number_str = (
        user.phone_number.decode("utf-8")
        if isinstance(user.phone_number, bytes)
        else user.phone_number
    )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value,
            "email": user.email,
            "phone_number": phone_number_str,
            "preferred_language": user.preferred_language.value
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": new_raw,
        "token_type": "bearer"
    }


# ============================================================
# CHANGE PASSWORD
# ============================================================
@router.post("/change-password")
async def change_password(
    db: AsyncSession = Depends(get_db),
    passwords: ChangePassword = Depends(),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(passwords.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )

    current_user.password = get_password_hash(passwords.new_password)
    current_user.password_changed = True

    db.add(current_user)
    await db.commit()

    return {"message": "Password changed successfully"}


# ============================================================
# FORGOT PASSWORD
# ============================================================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


@router.post("/forgot-password")
async def forgot_password(
    request_data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    email = request_data.email
    user = await get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)

    reset_link = (
        f"https://rental-user-management-frontend-sigma.vercel.app/reset-password?token={token}"
    )

    supabase.table("password_resets").insert({
        "user_id": str(user.id),
        "email": email,
        "token": token,
        "expires_at": expires_at.isoformat()
    }).execute()

    try:
        send_reset_email(email, reset_link)
        return {"message": "Reset link sent successfully"}
    except Exception as e:
        print("❌ EMAIL SEND ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to send reset email")


# ============================================================
# RESET PASSWORD
# ============================================================
class ResetPasswordRequest(BaseModel):
    token: str
    password: str


@router.post("/reset-password")
async def reset_password(
    request_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    token = request_data.token
    new_password = request_data.password

    result = (
        supabase.table("password_resets")
        .select("*")
        .eq("token", token)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=400, detail="Invalid token")

    reset_row = result.data[0]
    expires_at = datetime.fromisoformat(reset_row["expires_at"])

    if expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Expired token")

    user = await get_user(db, reset_row["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = get_password_hash(new_password)

    db.add(user)
    await db.commit()

    supabase.table("password_resets").delete().eq("token", token).execute()

    return {"message": "Password has been reset successfully."}


# ============================================================
# VERIFY TOKEN
# ============================================================
@router.get("/verify", response_model=UserTokenData)
async def verify_token(current_user: User = Depends(get_current_user)):
    phone_number_str = (
        current_user.phone_number.decode("utf-8")
        if isinstance(current_user.phone_number, bytes)
        else current_user.phone_number
    )

    return UserTokenData(
        user_id=current_user.id,
        role=current_user.role,
        email=current_user.email,
        phone_number=phone_number_str,
        preferred_language=current_user.preferred_language
    )
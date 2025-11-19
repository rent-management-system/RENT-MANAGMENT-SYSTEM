from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from ..dependencies.auth import get_current_user
from ..schemas.token import Token, RefreshToken, UserTokenData
from ..schemas.user import ChangePassword, User
from ..core.security import create_access_token, create_refresh_token, verify_password, get_password_hash, decode_token
from ..db.session import get_db
from ..crud import get_user_by_email, get_user, create_refresh_token_db, get_refresh_token_by_token, delete_refresh_token
from ..models.user import UserRole
from ..core.config import settings
from app.utils.send_email import send_reset_email
import jwt  # PyJWT

router = APIRouter()

# ---------------- Login / Refresh ---------------- #

@router.post("/login", response_model=Token)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    phone_number_str = user.phone_number.decode('utf-8') if isinstance(user.phone_number, bytes) else user.phone_number

    access_token_data = {
        "sub": str(user.id),
        "role": user.role.value,
        "email": user.email,
        "phone_number": phone_number_str,
        "preferred_language": user.preferred_language.value
    }
    access_token = create_access_token(data=access_token_data)

    refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    raw_refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    hashed_refresh_token = get_password_hash(raw_refresh_token)
    await create_refresh_token_db(db, user_id=user.id, token=hashed_refresh_token, expires_at=refresh_token_expires)

    return {"access_token": access_token, "refresh_token": raw_refresh_token, "token_type": "bearer"}

# ---------------- Forgot / Reset Password ---------------- #

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 60

@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    email = request_data.email
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a JWT token for password reset
    payload = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    }
    reset_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    reset_link = f"http://localhost:5174/reset-password?token={reset_token}"

    try:
        send_reset_email(email, reset_link)
        return {"message": "Reset link sent successfully"}
    except Exception as e:
        print("❌ Failed to send email:", e)
        raise HTTPException(status_code=500, detail="Failed to send reset email")

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    token = request_data.token
    new_password = request_data.password

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = get_password_hash(new_password)
    db.add(user)
    await db.commit()

    return {"message": "Password has been reset successfully."}

# ---------------- Verify Token ---------------- #

@router.get("/verify", response_model=UserTokenData)
async def verify_token(current_user: User = Depends(get_current_user)):
    phone_number_str = current_user.phone_number.decode('utf-8') if isinstance(current_user.phone_number, bytes) else current_user.phone_number
    return UserTokenData(
        user_id=current_user.id,
        role=current_user.role,
        email=current_user.email,
        phone_number=phone_number_str,
        preferred_language=current_user.preferred_language
    )

from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from ..models.user import UserRole, Language

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str

class UserTokenData(BaseModel):
    user_id: uuid.UUID
    role: UserRole
    email: EmailStr
    phone_number: Optional[str] = None
    preferred_language: Language
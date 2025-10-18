from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid
from app.models.user import UserRole, Language, Currency

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.TENANT
    phone_number: Optional[str] = Field(None, pattern=r"^\+251[79]\d{8}$")
    preferred_language: Language = Language.EN
    preferred_currency: Currency = Currency.ETB

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\+251[79]\d{8}$")
    preferred_language: Optional[Language] = None
    preferred_currency: Optional[Currency] = None

class UserInDBBase(UserBase):
    id: uuid.UUID
    role: UserRole
    is_active: bool
    password_changed: bool # Added password_changed

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: Optional[str] = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: str
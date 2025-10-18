from pydantic import BaseModel
from typing import Optional
import uuid

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: uuid.UUID
    role: str
    email: str
    phone_number: Optional[str] = None
    preferred_language: str

class RefreshToken(BaseModel):
    refresh_token: str

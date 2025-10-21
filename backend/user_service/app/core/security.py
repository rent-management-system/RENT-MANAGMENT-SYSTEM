from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from ..core.config import settings
from cryptography.fernet import Fernet
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate a key for AES-256 encryption
def generate_aes_key():
    return Fernet.generate_key().decode()

# Initialize Fernet with the AES_SECRET_KEY from settings
def get_fernet():
    if not settings.AES_SECRET_KEY:
        raise ValueError("AES_SECRET_KEY is not set in environment variables")
    return Fernet(settings.AES_SECRET_KEY.encode())

def encrypt_data(data: str) -> bytes:
    f = get_fernet()
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes) -> str:
    f = get_fernet()
    return f.decrypt(encrypted_data).decode()

def create_access_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.JWTError:
        return None  # Other JWT errors (e.g., invalid signature)
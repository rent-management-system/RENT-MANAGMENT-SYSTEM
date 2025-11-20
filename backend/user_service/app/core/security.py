from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from ..core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# AES encryption functions are no longer used for phone numbers.
# Keeping them commented out in case they are needed for other purposes in the future.
# from cryptography.fernet import Fernet
# import base64

# # Generate a key for AES-256 encryption
# def generate_aes_key():
#     return Fernet.generate_key().decode()

# # Initialize Fernet with the AES_SECRET_KEY from settings
# def get_fernet():
#     if not settings.AES_SECRET_KEY:
#         raise ValueError("AES_SECRET_KEY is not set in environment variables")
#     return Fernet(settings.AES_SECRET_KEY.encode())

# def encrypt_data(data: str) -> str:
#     f = get_fernet()
#     encrypted_bytes = f.encrypt(data.encode())
#     return base64.urlsafe_b64encode(encrypted_bytes).decode()

# def decrypt_data(encrypted_data_str: str) -> str:
#     f = get_fernet()
#     encrypted_bytes = base64.urlsafe_b64decode(encrypted_data_str.encode())
#     return f.decrypt(encrypted_bytes).decode()


def _truncate_password_to_safe_str(password: str) -> str:
    """
    Truncate the UTF-8 *bytes* representation of password to 72 bytes (bcrypt limit),
    then decode back to a str safely ignoring any partial multi-byte sequences.

    This guarantees the input passed to passlib is a `str` and <= 72 bytes when encoded.
    """
    if password is None:
        raise ValueError("password must be provided")
    if not isinstance(password, str):
        password = str(password)

    pw_bytes = password.encode('utf-8')[:72]
    safe_pw = pw_bytes.decode('utf-8', 'ignore')
    return safe_pw


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
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.JWT_ALGORITHM)
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
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the provided plain password against the stored hash.
    We truncate by bytes first (bcrypt limit) and pass a `str` to passlib.
    """
    safe_pw = _truncate_password_to_safe_str(plain_password)
    return pwd_context.verify(safe_pw, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash the password after truncating to 72 bytes and decoding to str.
    """
    safe_pw = _truncate_password_to_safe_str(password)
    return pwd_context.hash(safe_pw[:72])



def decode_token(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.JWTError:
        return None  # Other JWT errors (e.g., invalid signature)

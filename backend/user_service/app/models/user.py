import enum
import uuid
from datetime import datetime
from sqlalchemy import (Column, String, Boolean, DateTime, Enum as SAEnum, LargeBinary)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OWNER = "owner"
    TENANT = "tenant"
    BROKER = "broker"

class Language(str, enum.Enum):
    EN = "en"
    AM = "am"
    OM = "om"

class Currency(str, enum.Enum):
    ETB = "ETB"
    USD = "USD"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True) # Nullable for Google OAuth users
    full_name = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.TENANT)
    phone_number = Column(LargeBinary, nullable=True) # Encrypted
    preferred_language = Column(SAEnum(Language), default=Language.EN)
    preferred_currency = Column(SAEnum(Currency), default=Currency.ETB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_changed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

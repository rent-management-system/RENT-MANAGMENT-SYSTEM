from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    TENANT = "tenant"
    OWNER = "owner"
    ADMIN = "admin"
    BROKER = "broker"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    phone_number = Column(String(20), nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    google_id = Column(String(100), unique=True, nullable=True)
    properties = relationship("Property", back_populates="owner")

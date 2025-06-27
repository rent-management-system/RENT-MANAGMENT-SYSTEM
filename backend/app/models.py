# SQLAlchemy models
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    LANDLORD = "landlord"
    TENANT = "tenant"
    BROKER = "broker"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    google_id = Column(String, unique=True, nullable=True)
# CRUD operations
from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_or_get_oauth_user(db: Session, email: str, google_id: str, role: UserRole = UserRole.TENANT):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        db_user = User(email=email, google_id=google_id, role=role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        password=hashed_password,
        full_name=user.full_name, 
        role=user.role
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_or_get_oauth_user(
        db: Session, 
        email: str, 
        google_id: str, 
        full_name: str, 
        role: UserRole = UserRole.TENANT
        ):
    
    db_user = db.query(User).filter(User.google_id == google_id).first()
    if not db_user:
        db_user = User(email=email, google_id=google_id, full_name=full_name, role=role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

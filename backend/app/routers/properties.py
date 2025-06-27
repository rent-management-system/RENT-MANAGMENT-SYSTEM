from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Property as PropertyModel, User, UserRole
from app.schemas import PropertyCreate, Property
from app.dependencies import get_db, require_role

router = APIRouter(prefix="/properties", tags=["properties"])

@router.post("/", response_model=Property)
def create_property(
    property: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.OWNER))
):
    db_property = PropertyModel(**property.dict(), owner_id=current_user.id)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property
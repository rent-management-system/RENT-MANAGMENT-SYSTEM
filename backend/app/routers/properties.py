# Property-related endpoints
# In app/routers/properties.py
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
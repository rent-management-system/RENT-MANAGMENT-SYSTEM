from pydantic import BaseModel
from typing import Optional

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

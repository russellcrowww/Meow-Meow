from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class StaffBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100) 
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None)
    specialization: Optional[str] = Field(None,max_length=50)


class StaffCreate(StaffBase):
    pass


class StaffResponse(StaffBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StaffListResponse(BaseModel):
    staff: list[StaffResponse]
    total: int
    
    model_config = ConfigDict(from_attributes=True)
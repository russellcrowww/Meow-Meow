from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200) 
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None)
    price: int = Field(..., gt=0, description="Цена в рублях")
    duration: int = Field(..., gt=0, description="Длительность в минутах")

class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ServiceListResponse(BaseModel):
    services: list[ServiceResponse] 
    total: int
    
    model_config = ConfigDict(from_attributes=True)
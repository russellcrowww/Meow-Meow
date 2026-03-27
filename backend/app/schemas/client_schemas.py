from pydantic import BaseModel, Field, ConfigDict


class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200) 
    phone: str = Field(..., min_length=1, description = "Номер телефона RU")
    email: str = Field(...,min_length=1,  description = "Email")

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ClientListResponse(BaseModel):
    client: list[ClientResponse] 
    total: int
    model_config = ConfigDict(from_attributes=True)
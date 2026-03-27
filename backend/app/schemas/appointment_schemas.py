from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class AppointmentBase(BaseModel):
    start_time: datetime = Field(..., description="Время начала стрижки")
    # Статус по умолчанию (например, 'pending')
    status: str = Field("pending", max_length=20)

class AppointmentCreate(AppointmentBase):
    # Кого записываем, к кому и на что
    client_id: int
    staff_id: int
    service_id: int

class AppointmentResponse(AppointmentBase):
    id: int
    client_id: int
    staff_id: int
    service_id: int
    
    model_config = ConfigDict(from_attributes=True)

class AppointmentListResponse(BaseModel):
    appointments: list[AppointmentResponse] 
    total: int
    
    model_config = ConfigDict(from_attributes=True)


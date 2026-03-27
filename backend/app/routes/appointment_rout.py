from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.appointment_schemas import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import AppointmentService
from app.utils.telegram import send_tg_notification 

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment_in: AppointmentCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    service = AppointmentService(db)
    
    # 1. Создаем запись
    new_app = service.create_appointment(appointment_in)
    
    # 2. Получаем готовый текст сообщения из сервиса
    summary_text = service.get_appointment_summary(new_app.id)
    
    # 3. Отправляем в фоне через httpx
    background_tasks.add_task(send_tg_notification, summary_text)
    
    return new_app

@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.get_all_appointments()

@router.get("/staff/{staff_id}", response_model=list[AppointmentResponse])
def get_staff_schedule(staff_id: int, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.get_staff_schedule(staff_id)

@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    service = AppointmentService(db)
    return service.cancel_appointment(appointment_id)

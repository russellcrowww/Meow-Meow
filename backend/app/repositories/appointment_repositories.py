from typing import List, Optional
from sqlalchemy.orm import Session, joinedload 
from app.models.appointment import Appointment
from backend.app.schemas.appointment_schemas import AppointmentCreate 

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Appointment]:
        # Подгружаем всё сразу, чтобы в ответе были имена и названия
        return (
            self.db.query(Appointment)
            .options(
                joinedload(Appointment.client),
                joinedload(Appointment.staff),
                joinedload(Appointment.service)
            )
            .all()
        )
    
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        return (
            self.db.query(Appointment)
            .options(
                joinedload(Appointment.client),
                joinedload(Appointment.staff),
                joinedload(Appointment.service)
            )
            .filter(Appointment.id == appointment_id)
            .first()
        )

    def get_by_staff_id(self, staff_id: int) -> List[Appointment]:
        # Поиск всех записей конкретного мастера (для его расписания)
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.client), joinedload(Appointment.service))
            .filter(Appointment.staff_id == staff_id)
            .order_by(Appointment.start_time.asc()) # Сортируем по времени
            .all()
        )

    def get_by_client_id(self, client_id: int) -> List[Appointment]:
        # История посещений конкретного клиента
        return (
            self.db.query(Appointment)
            .options(joinedload(Appointment.staff), joinedload(Appointment.service))
            .filter(Appointment.client_id == client_id)
            .all()
        )

    def create(self, appointment_data: AppointmentCreate) -> Appointment:
        # Создаем запись. Важно: данные уже проверены Pydantic-схемой
        db_appointment = Appointment(**appointment_data.model_dump()) 
        self.db.add(db_appointment)
        self.db.commit() 
        self.db.refresh(db_appointment) 
        return db_appointment

    def update_status(self, appointment_id: int, new_status: str) -> Optional[Appointment]:
        # Метод для подтверждения или отмены записи (pending -> confirmed/cancelled)
        db_appointment = self.get_by_id(appointment_id)
        if db_appointment:
            db_appointment.status = new_status
            self.db.commit()
            self.db.refresh(db_appointment)
        return db_appointment
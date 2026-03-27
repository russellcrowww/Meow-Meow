from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.appointment_repositories import AppointmentRepository
from app.repositories.staff_repositories import StaffRepository
from backend.app.schemas.appointment_schemas import AppointmentCreate, AppointmentResponse

class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)
        self.staff_repo = StaffRepository(db) # Нужен для проверки существования мастера

    def create_appointment(self, appointment_data: AppointmentCreate) -> AppointmentResponse:
        # 1. Проверяем, существует ли мастер
        staff = self.staff_repo.get_by_id(appointment_data.staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Мастер не найден")

        # 2. ПРОВЕРКА ВРЕМЕНИ (Логика "Занято")
        # Ищем все записи этого мастера на этот день
        existing_appointments = self.repository.get_by_staff_id(appointment_data.staff_id)
        
        for app in existing_appointments:
            # Если время начала новой записи совпадает с уже существующей
            # (Тут можно усложнить, проверяя длительность услуги)
            if app.start_time == appointment_data.start_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Это время у мастера уже занято"
                )

        # 3. Если всё свободно — создаем запись
        return self.repository.create(appointment_data)

    def get_all_appointments(self) -> List[AppointmentResponse]:
        return self.repository.get_all()

    def cancel_appointment(self, appointment_id: int):
        # Меняем статус на 'cancelled' вместо физического удаления
        appointment = self.repository.update_status(appointment_id, "cancelled")
        if not appointment:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        return appointment

    def get_staff_schedule(self, staff_id: int) -> List[AppointmentResponse]:
        """Получить расписание конкретного мастера"""
        return self.repository.get_by_staff_id(staff_id)
    
    def get_appointment_summary(self, appointment_id: int) -> str:
        app = self.repository.get_by_id(appointment_id)
        if not app:
            return "Запись не найдена"
        return (
            f"<b>✂️ Новая запись в салон!</b>\n"
            f"<b>👤 Клиент:</b> {app.client.name} ({app.client.phone})\n"
            f"<b>💈 Мастер:</b> {app.staff.name}\n"
            f"<b>✨ Услуга:</b> {app.service.name}\n"
            f"<b>📅 Дата:</b> {app.start_time.strftime('%d.%m.%Y')}\n"
            f"<b>⏰ Время:</b> {app.start_time.strftime('%H:%M')}\n"
            f"<b>💰 Цена:</b> {app.service.price} руб."
        )

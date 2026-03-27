from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.service_repositories import ServiceRepository
from app.schemas.servise_schemas import ServiceCreate, ServiceResponse

class ServiceService:
    def __init__(self, db: Session):
        self.repository = ServiceRepository(db)

    def create_service(self, service_data: ServiceCreate) -> ServiceResponse:
        # 1. Проверяем, нет ли уже услуги с таким названием
        existing_service = self.repository.get_by_name(service_data.name)
        if existing_service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Услуга '{service_data.name}' уже есть в прайсе"
            )
        
        # 2. Если всё ок — создаем
        return self.repository.create(service_data)

    def get_all_services(self) -> List[ServiceResponse]:
        # Получаем весь список для прайса
        services = self.repository.get_all()
        if not services:
            return []
        return services

    def get_service_by_id(self, service_id: int) -> ServiceResponse:
        service = self.repository.get_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Услуга с ID {service_id} не найдена"
            )
        return service

    def update_service_price(self, service_id: int, new_price: float) -> ServiceResponse:
        # Бизнес-логика: цена не может быть нулевой
        if new_price <= 0:
            raise HTTPException(status_code=400, detail="Цена должна быть больше нуля")
            
        service = self.repository.get_by_id(service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Услуга не найдена")
            
        service.price = new_price
        # Здесь мы можем напрямую закоммитить изменения через сессию репозитория
        self.repository.db.commit()
        self.repository.db.refresh(service)
        return service

    def remove_service(self, service_id: int):
        # Проверяем существование перед удалением
        success = self.repository.delete(service_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось удалить: услуга не найдена"
            )
        return {"message": f"Услуга {service_id} успешно удалена из базы"}

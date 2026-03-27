from typing import List, Optional
from sqlalchemy.orm import Session, joinedload 
from app.models.service import Service
from app.schemas.servise_schemas import ServiceCreate 

class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Service]:
        return self.db.query(Service).options(joinedload(Service.staffs)).all()
    
    def get_by_id(self, service_id: int) -> Optional[Service]:
        return (
            self.db.query(Service)
            .options(joinedload(Service.staffs))
            .filter(Service.id == service_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Service]:
        # Поиск услуги по названию (например, для проверки дубликатов)
        return self.db.query(Service).filter(Service.name == name).first()

    def get_by_price_range(self, min_price: float, max_price: float) -> List[Service]:
        # Полезная фича для фильтрации на фронтенде
        return (
            self.db.query(Service)
            .filter(Service.price >= min_price, Service.price <= max_price)
            .all()
        )

    def create(self, service_data: ServiceCreate) -> Service:
        # Превращаем Pydantic-схему в SQLAlchemy-объект
        db_service = Service(**service_data.model_dump()) 
        self.db.add(db_service)
        self.db.commit() 
        self.db.refresh(db_service) 
        return db_service

    def delete(self, service_id: int) -> bool:
        db_service = self.get_by_id(service_id)
        if db_service:
            self.db.delete(db_service)
            self.db.commit()
            return True
        return False


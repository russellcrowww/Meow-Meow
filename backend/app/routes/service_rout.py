from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.servise_schemas import ServiceCreate, ServiceResponse
from app.services.service_service import ServiceService

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceResponse)
def create_service(service_in: ServiceCreate, db: Session = Depends(get_db)):
    service = ServiceService(db)
    return service.create_service(service_in)

@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    service = ServiceService(db)
    return service.get_all_services()
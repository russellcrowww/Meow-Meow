from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.client_schemas import ClientCreate, ClientResponse
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def get_or_create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.get_or_create_client(client_in)

@router.get("/{phone}", response_model=ClientResponse)
def get_client_by_phone(phone: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.find_client_by_phone(phone)

@router.get("/", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.get_all_clients()

@router.get("/{email}", response_model=ClientResponse)
def get_client_by_email(email: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.find_client_by_phone(email)


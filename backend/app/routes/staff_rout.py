from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.staff_schemas import StaffCreate, StaffResponse
from app.services.staff_service import StaffService

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(staff_in: StaffCreate, db: Session = Depends(get_db)):
    service = StaffService(db)
    return service.create_new_staff(staff_in)

@router.get("/", response_model=list[StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    service = StaffService(db)
    return service.get_all_staff()

@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    service = StaffService(db)
    return service.get_staff_by_id(staff_id)

@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    service = StaffService(db)
    return service.delete_staff(staff_id)

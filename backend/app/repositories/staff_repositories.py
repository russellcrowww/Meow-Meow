from typing import List, Optional
from sqlalchemy.orm import Session, joinedload 
from ..models.staff import Staff
from ..schemas.staff_schemas import StaffCreate

class StaffRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Staff]:
        return self.db.query(Staff).options(joinedload(Staff.services)).all()
    
    def get_by_id(self, staff_id: int) -> Optional[Staff]:
        return (
            self.db.query(Staff)
            .options(joinedload(Staff.services))
            .filter(Staff.id == staff_id)
            .first()
        )
    
    def get_by_specialization(self, spec: str) -> List[Staff]:
        return (
            self.db.query(Staff)
            .options(joinedload(Staff.services))
            .filter(Staff.specialization == spec)
            .all()
        )

    def create(self, staff_data: StaffCreate) -> Staff:
        db_staff = Staff(**staff_data.model_dump()) 
        self.db.add(db_staff)
        self.db.commit() 
        self.db.refresh(db_staff) 
        return db_staff

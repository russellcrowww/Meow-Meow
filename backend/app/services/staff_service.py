from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.staff_repositories import StaffRepository
from app.schemas.staff_schemas import StaffCreate, StaffResponse

class StaffService:
    def __init__(self, db: Session):
        self.repository = StaffRepository(db)

    def create_new_staff(self, staff_data: StaffCreate) -> StaffResponse:
        # 1. Проверяем, нет ли уже мастера с таким именем
        existing_staff = self.repository.get_by_name(staff_data.name)
        if existing_staff:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Мастер с именем {staff_data.name} уже существует"
            )
        
        # 2. Если всё ок — создаем через репозиторий
        return self.repository.create(staff_data)

    def get_all_staff(self) -> List[StaffResponse]:
        staff_list = self.repository.get_all()
        if not staff_list:
            return []
        return staff_list

    def get_staff_by_id(self, staff_id: int) -> StaffResponse:
        staff = self.repository.get_by_id(staff_id)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Мастер с ID {staff_id} не найден"
            )
        return staff

    def delete_staff(self, staff_id: int):
        # Здесь можно добавить проверку: нет ли у мастера будущих записей
        success = self.repository.delete(staff_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось удалить: мастер не найден"
            )
        return {"message": "Мастер успешно удален"}

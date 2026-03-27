from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.client_repositories import ClientRepository
from app.schemas.client_schemas import ClientCreate, ClientResponse

class ClientService:
    def __init__(self, db: Session):
        self.repository = ClientRepository(db)

    def get_or_create_client(self, client_data: ClientCreate) -> ClientResponse:
        """
        Проверяет по номеру телефона: если клиент новый — создает,
        если старый — возвращает его данные.
        """
        # 1. Ищем по телефону в базе (через репозиторий)
        existing_client = self.repository.get_by_phone(client_data.phone)
        
        if existing_client:
            # Если нашли, просто возвращаем его (можно обновить имя, если оно изменилось)
            return existing_client
        
        # 2. Если не нашли — создаем новую запись
        return self.repository.create(client_data)

    def get_all_clients(self) -> List[ClientResponse]:
        return self.repository.get_all()

    def get_client_by_id(self, client_id: int) -> ClientResponse:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Клиент с ID {client_id} не найден"
            )
        return client

    def find_client_by_phone(self, phone: str) -> ClientResponse:
        client = self.repository.get_by_phone(phone)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент с таким номером телефона не зарегистрирован"
            )
        return client

    def find_client_by_email(self, email: str) -> ClientResponse:
        client = self.repository.get_by_email(email)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент с такой почтой не зарегистрирован"
            )
        return client
    



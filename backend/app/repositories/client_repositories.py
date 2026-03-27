from typing import List, Optional
from sqlalchemy.orm import Session, joinedload 
from app.models.client import Client
from app.schemas.client_schemas import ClientCreate 

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Client]:
        # Подгружаем историю записей клиента, если нужно
        return self.db.query(Client).options(joinedload(Client.appointments)).all()
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        return (
            self.db.query(Client)
            .options(joinedload(Client.appointments))
            .filter(Client.id == client_id)
            .first()
        )

    def get_by_phone(self, phone: str) -> Optional[Client]:
        # проверяем, был ли клиент у нас раньше
        return (
            self.db.query(Client)
            .options(joinedload(Client.appointments))
            .filter(Client.phone == phone)
            .first()
        )
    
    def get_by_email(self, email: str) -> Optional[Client]:
        # проверяем, был ли клиент у нас раньше
        return (
            self.db.query(Client)
            .options(joinedload(Client.appointments))
            .filter(Client.email == email)
            .first()
        )

    def get_by_name(self, name: str) -> List[Client]:
        # Поиск по имени 
        return (
            self.db.query(Client)
            .filter(Client.name.ilike(f"%{name}%")) # ilike  поиск без учета регистра
            .all()
        )

    def create(self, client_data: ClientCreate) -> Client:
        # Сохраняем нового клиента
        db_client = Client(**client_data.model_dump()) 
        self.db.add(db_client)
        self.db.commit() 
        self.db.refresh(db_client) 
        return db_client

    def update(self, client_id: int, client_data: ClientCreate) -> Optional[Client]:
        # Если клиент сменил почту или имя
        db_client = self.get_by_id(client_id)
        if db_client:
            for key, value in client_data.model_dump().items():
                setattr(db_client, key, value)
            self.db.commit()
            self.db.refresh(db_client)
        return db_client

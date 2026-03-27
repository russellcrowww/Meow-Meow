from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship    
from ..database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True)

    # Связь с записями (у клиента может быть много стрижек)
    appointments = relationship("Appointment", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', phone='{self.phone}')>"
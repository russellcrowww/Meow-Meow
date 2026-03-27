from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship   
from ..database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ссылки на тех, кто участвует в процессе
    client_id = Column(Integer, ForeignKey("clients.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))
    service_id = Column(Integer, ForeignKey("service.id"))
    
    # Время записи
    start_time = Column(DateTime, nullable=False)
    # Статус: 'pending' (ожидание), 'confirmed' (подтверждено), 'cancelled' (отмена)
    status = Column(String, default="pending")

    # Обратные связи для удобства получения данных
    client = relationship("Client", back_populates="appointments")
    staff = relationship("Staff", back_populates="appointments")
    service = relationship("Service")

    def __repr__(self):
        return f"<Appointment(id={self.id}, time='{self.start_time}', status='{self.status}')>"
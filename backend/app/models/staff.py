from sqlalchemy import Column, Integer, String, ForeignKey, Text as SQLText,Table
from sqlalchemy.orm import relationship    
from ..database import Base

staff_service_association = Table(
    "staff_service_association",
    Base.metadata,
    Column("staff_id", Integer, ForeignKey("staff.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("service.id"), primary_key=True)
)

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(SQLText) 
    image_url = Column(String)
    specialization = Column(SQLText)
    
    services = relationship("Service", secondary=staff_service_association, back_populates="staffs")
    appointments = relationship("Appointment", back_populates="staff")

    def __repr__(self):
        return f"<Staff(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"
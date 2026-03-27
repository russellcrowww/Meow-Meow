from sqlalchemy import Column, Integer, String,  ForeignKey, Text as SQLText, Float,Table
from sqlalchemy.orm import relationship     
from ..database import Base

staff_service_association = Table("staff_service",
    Base.metadata,
    Column("staff_id", Integer, ForeignKey("staff.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("service.id"), primary_key=True)
)

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(SQLText,nullable=False) 
    image_url = Column(String)
    price = Column(Float,nullable=False)
    duration = Column(Integer,nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    
    staffs = relationship(
        "Staff", 
        secondary=staff_service_association, 
        back_populates="services"
    )

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', staff_id='{self.staff_id}')>"
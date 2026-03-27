from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime     
from ..database import Base
from sqlalchemy.orm import relationship

class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    color = Column(String, nullable=False)
    hunger = Column(Integer, default=100,nullable=False)    
    happiness = Column(Integer, default=100,nullable=False) 
    energy = Column(Integer, default=100, nullable=False )    
    last_fed = Column(DateTime, default=datetime.utcnow)
    last_sleep = Column(DateTime, default=datetime.utcnow)
    coins = Column(Integer, default=100)

    action = relationship("Action", back_populates="Cat")

    def __repr__(self):
        return f"<Cat(name='{self.name}', hunger={self.hunger})>"

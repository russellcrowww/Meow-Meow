from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime     
from ..database import Base

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    satiety_bonus = Column(Integer,default=100,nullable=False)
    price = Column(Integer,nullable=False)
    happiness_bonus = Column(Integer,default=100,nullable=False)

    
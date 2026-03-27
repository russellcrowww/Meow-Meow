from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime     
from ..database import Base
from sqlalchemy.orm import relationship

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"))
    item_id = Column(Integer, ForeignKey("item.id"))
    quantity = Column(Integer, default=1) # Сколько штук купили


    cat = relationship("Cat", back_populates="inventory")
    item = relationship("Item") 
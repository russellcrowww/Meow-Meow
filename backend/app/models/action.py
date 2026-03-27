from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime     
from ..database import Base
from sqlalchemy.orm import relationship

class Action(Base):
    __tablename__ = "action"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id")) 
    action_name = Column(String) 
    points = Column(Integer)  
    timestamp = Column(DateTime, default=datetime.utcnow)

    cat = relationship("cat", back_populates="action")
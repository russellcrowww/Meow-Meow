from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from config import settings


engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#объявление Base
class Base(DeclarativeBase):
    pass

#генератор сессии с типизацией
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    #Создаст таблицы если их нет
    Base.metadata.create_all(bind=engine)

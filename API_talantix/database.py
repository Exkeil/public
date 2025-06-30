from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ApiData(Base):
    __tablename__ = "api_data"
    id = Column(Integer, primary_key=True)
    object_type = Column(String, index=True)
    external_id = Column(String, index=True)
    data = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_system = Column(Boolean)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    yield db
    db.close() 
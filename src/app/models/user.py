from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    hashed_password = Column(String)
    cpf = Column(String, unique=True, index=True)
    birth_date = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)

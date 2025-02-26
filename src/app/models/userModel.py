from sqlalchemy import Column, Integer, String, Date, DateTime, func
from app.config.database import Base

class User(Base):
    __tablename__ = "tb_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

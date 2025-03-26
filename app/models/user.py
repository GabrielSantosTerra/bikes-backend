from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    telefone_celular = Column(String, nullable=True)
    telefone_fixo = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    data_nascimento = Column(String, nullable=True)
    tipo_pessoa = Column(String, nullable=True)

    usuario = relationship("Usuario", back_populates="pessoa")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    pessoa = relationship("Pessoa", back_populates="usuario")

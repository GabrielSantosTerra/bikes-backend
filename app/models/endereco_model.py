from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    cep = Column(String(20), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    id_cidade = Column(Integer, ForeignKey("cidades.id"), nullable=True)
    nome_cidade = Column(String(100), nullable=True)
    nome_estado = Column(String(100), nullable=True)
    endereco_primario = Column(Boolean, default=False)

    pessoa = relationship("Pessoa")
    cidade = relationship("Cidade")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    cep = Column(String(20), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(255))
    bairro = Column(String(255), nullable=False)
    id_cidade = Column(Integer, ForeignKey("cidades.id"), nullable=False)
    nome_cidade = Column(String(100))
    nome_estado = Column(String(100))

    pessoa = relationship("Pessoa")
    cidade = relationship("Cidade")

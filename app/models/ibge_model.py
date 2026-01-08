from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo_iso = Column(String(10), nullable=False)

    estados = relationship("Estado", back_populates="pais")


class Regiao(Base):
    __tablename__ = "regioes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

    estados = relationship("Estado", back_populates="regiao")
    cidades = relationship("Cidade", back_populates="regiao")


class Estado(Base):
    __tablename__ = "estados"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sigla = Column(String(2), nullable=False)
    id_pais = Column(Integer, ForeignKey("paises.id"), nullable=False)
    id_regiao = Column(Integer, ForeignKey("regioes.id"), nullable=False)

    pais = relationship("Pais", back_populates="estados")
    regiao = relationship("Regiao", back_populates="estados")
    cidades = relationship("Cidade", back_populates="estado")


class Cidade(Base):
    __tablename__ = "cidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo_ibge = Column(Integer, unique=True, nullable=False)
    codigo_regiao = Column(Integer, ForeignKey("regioes.id"), nullable=False)
    id_estado = Column(Integer, ForeignKey("estados.id"), nullable=False)

    regiao = relationship("Regiao", back_populates="cidades")
    estado = relationship("Estado", back_populates="cidades")

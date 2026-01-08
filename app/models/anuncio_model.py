from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class AnuncioBike(Base):
    __tablename__ = "anuncio_bikes"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)

    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)

    marca = Column(String(100), nullable=True)
    modelo = Column(String(100), nullable=True)
    aro = Column(String(20), nullable=True)
    tamanho = Column(String(50), nullable=True)
    cor = Column(String(50), nullable=True)

    condicao = Column(String(50), nullable=True)
    preco = Column(Numeric(15, 2), nullable=False)

    status = Column(String(30), nullable=False, default="ativo")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pessoa = relationship("Pessoa")


class AnuncioAcessorio(Base):
    __tablename__ = "anuncio_acessorios"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)

    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)

    categoria = Column(String(100), nullable=True)
    marca = Column(String(100), nullable=True)

    condicao = Column(String(50), nullable=True)
    preco = Column(Numeric(15, 2), nullable=False)

    status = Column(String(30), nullable=False, default="ativo")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pessoa = relationship("Pessoa")


class AnuncioPeca(Base):
    __tablename__ = "anuncio_pecas"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)

    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=True)

    tipo_peca = Column(String(100), nullable=True)
    marca = Column(String(100), nullable=True)
    compatibilidade = Column(String(200), nullable=True)

    condicao = Column(String(50), nullable=True)
    preco = Column(Numeric(15, 2), nullable=False)

    status = Column(String(30), nullable=False, default="ativo")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pessoa = relationship("Pessoa")

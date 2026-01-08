from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Eventos(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    nome = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    valor = Column(float, nullable=False)
    data_ini = Column(String, nullable=False)
    data_fim = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    lotes = relationship("Lotes", back_populates="eventos")
    inscricoes = relationship("Inscricoes", back_populates="eventos")

class Lotes(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    id_evento = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    n_lotes = Column(Integer, nullable=False)
    valor = Column(float, nullable=False)
    total_inscricoes = Column(Integer, nullable=False)
    data_ini = Column(String, nullable=False)
    data_fim = Column(String, nullable=False)

    eventos = relationship("Eventos", back_populates="lotes")

class Inscricoes(Base):
    __tablename__ = "inscricoes"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    id_evento = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    nome = Column(String, ForeignKey("pessoas.nome"), nullable=False)
    id_lote = Column(Integer, ForeignKey("lotes.id"), nullable=False)
    id_pagamento = Column(Integer, ForeignKey("pagamentos.id"), nullable=False)
    brinde_retirado = Column(String, nullable=False)

    eventos = relationship("Eventos", back_populates="inscricoes")

class FormasPagamento(Base):
    __tablename__ = "formas_pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    formato = Column(String, nullable=False)

    inscricoes = relationship("Inscricoes", back_populates="pagamentos")

class Brindes(Base):
    __tablename__ = "brindes"

    id = Column(Integer, primary_key=True, index=True)
    id_evento = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    n_lotes = Column(Integer, nullable=False)
    brinde = Column(String, nullable=False)


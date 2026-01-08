from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.database.connection import Base


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
    id_anuncio = Column(Integer, nullable=False)

    # bikes | acessorios | pecas
    tipo_anuncio = Column(String(30), nullable=False)

    quantidade = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("id_anuncio", "tipo_anuncio", name="uq_estoque_anuncio_tipo"),
    )

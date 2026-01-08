from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioAcessorio
from app.models.estoque_model import Estoque

from app.schemas.anuncio_schema import (
    AnuncioAcessorioCreateWithEstoque,
    AnuncioAcessorioResponseWithEstoque,
    AnuncioAcessorioUpdate,
    AnuncioAcessorioOut,
)

router = APIRouter(prefix="/anuncios/acessorios", tags=["Anúncios - Acessórios"])


# -----------------------------------------
# POST (novo) - cria anúncio + estoque
# -----------------------------------------
@router.post("/", response_model=AnuncioAcessorioResponseWithEstoque)
def create_anuncio_acessorio(payload: AnuncioAcessorioCreateWithEstoque, db: Session = Depends(get_db)):
    tipo_anuncio = "acessorios"

    anuncio = AnuncioAcessorio(**payload.anuncio.model_dump())
    db.add(anuncio)
    db.flush()

    estoque = Estoque(
        id_anuncio=anuncio.id,
        tipo_anuncio=tipo_anuncio,
        quantidade=payload.estoque.quantidade,
    )
    db.add(estoque)

    db.commit()
    db.refresh(anuncio)
    db.refresh(estoque)

    return {"anuncio": anuncio, "estoque": estoque}


# -----------------------------------------
# GET - retorna anúncio (como antes)
# -----------------------------------------
@router.get("/{anuncio_id}", response_model=AnuncioAcessorioOut)
def get_anuncio_acessorio(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioAcessorio).filter(AnuncioAcessorio.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (acessório) não encontrado.")
    return anuncio


# -----------------------------------------
# PUT - atualiza anúncio (como antes)
# -----------------------------------------
@router.put("/{anuncio_id}", response_model=AnuncioAcessorioOut)
def update_anuncio_acessorio(anuncio_id: int, payload: AnuncioAcessorioUpdate, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioAcessorio).filter(AnuncioAcessorio.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (acessório) não encontrado.")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(anuncio, k, v)

    db.commit()
    db.refresh(anuncio)
    return anuncio

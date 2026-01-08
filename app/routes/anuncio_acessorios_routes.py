from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioAcessorio
from app.schemas.anuncio_schema import (
    AnuncioAcessorioCreate,
    AnuncioAcessorioUpdate,
    AnuncioAcessorioOut,
)

router = APIRouter(prefix="/anuncios/acessorios", tags=["Anúncios - Acessórios"])


@router.post("/", response_model=AnuncioAcessorioOut)
def create_anuncio_acessorio(payload: AnuncioAcessorioCreate, db: Session = Depends(get_db)):
    anuncio = AnuncioAcessorio(**payload.model_dump())
    db.add(anuncio)
    db.commit()
    db.refresh(anuncio)
    return anuncio


@router.get("/{anuncio_id}", response_model=AnuncioAcessorioOut)
def get_anuncio_acessorio(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioAcessorio).filter(AnuncioAcessorio.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (acessório) não encontrado.")
    return anuncio


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

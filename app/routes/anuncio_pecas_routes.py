from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioPeca
from app.schemas.anuncio_schema import (
    AnuncioPecaCreate,
    AnuncioPecaUpdate,
    AnuncioPecaOut,
)

router = APIRouter(prefix="/anuncios/pecas", tags=["Anúncios - Peças"])


@router.post("/", response_model=AnuncioPecaOut)
def create_anuncio_peca(payload: AnuncioPecaCreate, db: Session = Depends(get_db)):
    anuncio = AnuncioPeca(**payload.model_dump())
    db.add(anuncio)
    db.commit()
    db.refresh(anuncio)
    return anuncio


@router.get("/{anuncio_id}", response_model=AnuncioPecaOut)
def get_anuncio_peca(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioPeca).filter(AnuncioPeca.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (peça) não encontrado.")
    return anuncio


@router.put("/{anuncio_id}", response_model=AnuncioPecaOut)
def update_anuncio_peca(anuncio_id: int, payload: AnuncioPecaUpdate, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioPeca).filter(AnuncioPeca.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (peça) não encontrado.")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(anuncio, k, v)

    db.commit()
    db.refresh(anuncio)
    return anuncio

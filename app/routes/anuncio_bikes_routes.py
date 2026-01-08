from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioBike
from app.schemas.anuncio_schema import (
    AnuncioBikeCreate,
    AnuncioBikeUpdate,
    AnuncioBikeOut,
)

router = APIRouter(prefix="/anuncios/bikes", tags=["Anúncios - Bikes"])


@router.post("/", response_model=AnuncioBikeOut)
def create_anuncio_bike(payload: AnuncioBikeCreate, db: Session = Depends(get_db)):
    anuncio = AnuncioBike(**payload.model_dump())
    db.add(anuncio)
    db.commit()
    db.refresh(anuncio)
    return anuncio


@router.get("/{anuncio_id}", response_model=AnuncioBikeOut)
def get_anuncio_bike(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioBike).filter(AnuncioBike.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (bike) não encontrado.")
    return anuncio


@router.put("/{anuncio_id}", response_model=AnuncioBikeOut)
def update_anuncio_bike(anuncio_id: int, payload: AnuncioBikeUpdate, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioBike).filter(AnuncioBike.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (bike) não encontrado.")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(anuncio, k, v)

    db.commit()
    db.refresh(anuncio)
    return anuncio

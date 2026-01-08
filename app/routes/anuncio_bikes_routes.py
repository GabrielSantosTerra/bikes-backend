from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioBike
from app.models.estoque_model import Estoque

from app.schemas.anuncio_schema import (
    AnuncioBikeCreateWithEstoque,
    AnuncioBikeResponseWithEstoque,
    AnuncioBikeUpdate,
    AnuncioBikeOut,
)

router = APIRouter(prefix="/anuncios/bikes", tags=["Anúncios - Bikes"])


# -----------------------------------------
# POST (novo) - cria anúncio + estoque
# -----------------------------------------
@router.post("/", response_model=AnuncioBikeResponseWithEstoque)
def create_anuncio_bike(payload: AnuncioBikeCreateWithEstoque, db: Session = Depends(get_db)):
    tipo_anuncio = "bikes"

    anuncio = AnuncioBike(**payload.anuncio.model_dump())
    db.add(anuncio)
    db.flush()  # garante anuncio.id antes do commit

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
@router.get("/{anuncio_id}", response_model=AnuncioBikeOut)
def get_anuncio_bike(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioBike).filter(AnuncioBike.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (bike) não encontrado.")
    return anuncio


# -----------------------------------------
# PUT - atualiza anúncio (como antes)
# -----------------------------------------
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

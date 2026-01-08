from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioPeca
from app.models.estoque_model import Estoque

from app.schemas.anuncio_schema import (
    AnuncioPecaCreateWithEstoque,
    AnuncioPecaResponseWithEstoque,
)

router = APIRouter(prefix="/anuncios/pecas", tags=["Anúncios - Peças"])
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.anuncio_model import AnuncioPeca
from app.models.estoque_model import Estoque

from app.schemas.anuncio_schema import (
    AnuncioPecaCreateWithEstoque,
    AnuncioPecaResponseWithEstoque,
    AnuncioPecaUpdate,
    AnuncioPecaOut,
)

router = APIRouter(prefix="/anuncios/pecas", tags=["Anúncios - Peças"])


# -----------------------------------------
# POST (novo) - cria anúncio + estoque
# -----------------------------------------
@router.post("/", response_model=AnuncioPecaResponseWithEstoque)
def create_anuncio_peca(payload: AnuncioPecaCreateWithEstoque, db: Session = Depends(get_db)):
    tipo_anuncio = "pecas"

    anuncio = AnuncioPeca(**payload.anuncio.model_dump())
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
@router.get("/{anuncio_id}", response_model=AnuncioPecaOut)
def get_anuncio_peca(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(AnuncioPeca).filter(AnuncioPeca.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio (peça) não encontrado.")
    return anuncio


# -----------------------------------------
# PUT - atualiza anúncio (como antes)
# -----------------------------------------
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


@router.post("/", response_model=AnuncioPecaResponseWithEstoque)
def create_anuncio_peca(payload: AnuncioPecaCreateWithEstoque, db: Session = Depends(get_db)):
    tipo_anuncio = "pecas"

    anuncio = AnuncioPeca(**payload.anuncio.model_dump())
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

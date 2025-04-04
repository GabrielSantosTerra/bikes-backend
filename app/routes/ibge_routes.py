from app.models.ibge_model import Pais, Regiao, Estado, Cidade
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.database.connection import get_db
from fastapi import APIRouter

router = APIRouter()

@router.get("/localidades/paises")
def get_paises(db: Session = Depends(get_db)):
    paises = db.query(Pais).all()
    return [{"id": p.id, "nome": p.nome} for p in paises]

@router.get("/localidades/regioes")
def get_regioes(db: Session = Depends(get_db)):
    regioes = db.query(Regiao).all()
    return [{"id": r.id, "nome": r.nome} for r in regioes]

@router.get("/localidades/estados")
def get_estados(regiao_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Estado)
    if regiao_id:
        query = query.filter(Estado.id_regiao == regiao_id)
    estados = query.all()
    return [{"id": e.id, "nome": e.nome, "sigla": e.sigla} for e in estados]

@router.get("/localidades/cidades")
def get_cidades(estado_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Cidade)
    if estado_id:
        query = query.filter(Cidade.id_estado == estado_id)
    cidades = query.all()
    return [{"id": c.id, "nome": c.nome, "id_estado": c.id_estado} for c in cidades]


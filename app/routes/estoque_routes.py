from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.estoque_model import Estoque
from app.models.anuncio_model import AnuncioBike, AnuncioAcessorio, AnuncioPeca
from app.models.user_model import Pessoa, Usuario

from app.schemas.estoque_schema import (
    EstoqueCreateNested,
    EstoqueUpdateNested,
    EstoqueResponseNested,
    EstoqueOut,
    PessoaResponse,
)
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/estoque", tags=["Estoque"])


def _resolve_pessoa_id_by_anuncio(db: Session, tipo_anuncio: str, id_anuncio: int) -> int:
    tipo = (tipo_anuncio or "").strip().lower()

    if tipo == "bikes":
        anuncio = db.query(AnuncioBike).filter(AnuncioBike.id == id_anuncio).first()
    elif tipo == "acessorios":
        anuncio = db.query(AnuncioAcessorio).filter(AnuncioAcessorio.id == id_anuncio).first()
    elif tipo == "pecas":
        anuncio = db.query(AnuncioPeca).filter(AnuncioPeca.id == id_anuncio).first()
    else:
        raise HTTPException(status_code=400, detail="tipo_anuncio inválido. Use: bikes | acessorios | pecas")

    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado para o tipo informado.")

    return anuncio.id_pessoa


def _build_response(db: Session, estoque_row: Estoque) -> EstoqueResponseNested:
    pessoa_id = _resolve_pessoa_id_by_anuncio(db, estoque_row.tipo_anuncio, estoque_row.id_anuncio)

    pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa vinculada ao anúncio não encontrada.")

    usuario = db.query(Usuario).filter(Usuario.id_pessoa == pessoa_id).first()

    pessoa_out = PessoaResponse(
        nome_completo=pessoa.nome_completo,
        cpf_cnpj=pessoa.cpf_cnpj,
        email=pessoa.email,
        telefone_celular=getattr(pessoa, "telefone_celular", None),
        data_nascimento=str(getattr(pessoa, "data_nascimento", None)) if getattr(pessoa, "data_nascimento", None) else None,
        tipo_pessoa=pessoa.tipo_pessoa,
        fantasia=getattr(pessoa, "fantasia", None),
        regime=getattr(pessoa, "regime", None),
    )

    usuario_out = None
    if usuario:
        # Seu UserResponse espera: nome, cpf, nascimento, telefone, email
        usuario_out = UserResponse(
            nome=pessoa.nome_completo,
            cpf=pessoa.cpf_cnpj,
            nascimento=str(getattr(pessoa, "data_nascimento", None)) if getattr(pessoa, "data_nascimento", None) else None,
            telefone=getattr(pessoa, "telefone_celular", None),
            email=pessoa.email,
        )

    estoque_out = EstoqueOut(
        id=estoque_row.id,
        id_anuncio=estoque_row.id_anuncio,
        tipo_anuncio=estoque_row.tipo_anuncio,
        quantidade=estoque_row.quantidade,
    )

    return EstoqueResponseNested(
        pessoa=pessoa_out,
        usuario=usuario_out,
        estoque=estoque_out,
    )


@router.post("/", response_model=EstoqueResponseNested)
def create_or_update_estoque(payload: EstoqueCreateNested, db: Session = Depends(get_db)):
    id_anuncio = payload.anuncio.id_anuncio
    tipo_anuncio = payload.anuncio.tipo_anuncio.strip().lower()
    quantidade = payload.estoque.quantidade

    # valida se o anúncio existe e resolve o owner (pessoa)
    _ = _resolve_pessoa_id_by_anuncio(db, tipo_anuncio, id_anuncio)

    row = (
        db.query(Estoque)
        .filter(Estoque.id_anuncio == id_anuncio, Estoque.tipo_anuncio == tipo_anuncio)
        .first()
    )

    if row:
        row.quantidade = quantidade
    else:
        row = Estoque(id_anuncio=id_anuncio, tipo_anuncio=tipo_anuncio, quantidade=quantidade)
        db.add(row)

    db.commit()
    db.refresh(row)
    return _build_response(db, row)


@router.get("/{tipo_anuncio}/{id_anuncio}", response_model=EstoqueResponseNested)
def get_estoque(tipo_anuncio: str, id_anuncio: int, db: Session = Depends(get_db)):
    tipo = tipo_anuncio.strip().lower()

    row = db.query(Estoque).filter(Estoque.id_anuncio == id_anuncio, Estoque.tipo_anuncio == tipo).first()
    if not row:
        raise HTTPException(status_code=404, detail="Estoque não encontrado para este anúncio.")

    return _build_response(db, row)


@router.put("/{tipo_anuncio}/{id_anuncio}", response_model=EstoqueResponseNested)
def update_estoque(tipo_anuncio: str, id_anuncio: int, payload: EstoqueUpdateNested, db: Session = Depends(get_db)):
    tipo = tipo_anuncio.strip().lower()

    row = db.query(Estoque).filter(Estoque.id_anuncio == id_anuncio, Estoque.tipo_anuncio == tipo).first()
    if not row:
        raise HTTPException(status_code=404, detail="Estoque não encontrado para este anúncio.")

    row.quantidade = payload.estoque.quantidade

    db.commit()
    db.refresh(row)
    return _build_response(db, row)

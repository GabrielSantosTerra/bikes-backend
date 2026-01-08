from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ---------------------------
# Estoque (shared)
# ---------------------------

class EstoqueInfo(BaseModel):
    quantidade: int = 0


class EstoqueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_anuncio: int
    tipo_anuncio: str
    quantidade: int


# ---------------------------
# BIKES
# ---------------------------

class AnuncioBikeCreate(BaseModel):
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    aro: Optional[str] = None
    tamanho: Optional[str] = None
    cor: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: Optional[str] = "ativo"

class AnuncioBikeUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    aro: Optional[str] = None
    tamanho: Optional[str] = None
    cor: Optional[str] = None
    condicao: Optional[str] = None
    preco: Optional[Decimal] = None
    status: Optional[str] = None

class AnuncioBikeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    aro: Optional[str] = None
    tamanho: Optional[str] = None
    cor: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: str
    created_at: datetime
    updated_at: datetime


class AnuncioBikeCreateWithEstoque(BaseModel):
    anuncio: AnuncioBikeCreate
    estoque: EstoqueInfo


class AnuncioBikeResponseWithEstoque(BaseModel):
    anuncio: AnuncioBikeOut
    estoque: EstoqueOut


# ---------------------------
# ACESSÓRIOS
# ---------------------------

class AnuncioAcessorioCreate(BaseModel):
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: Optional[str] = "ativo"

class AnuncioAcessorioUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    condicao: Optional[str] = None
    preco: Optional[Decimal] = None
    status: Optional[str] = None

class AnuncioAcessorioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: str
    created_at: datetime
    updated_at: datetime


class AnuncioAcessorioCreateWithEstoque(BaseModel):
    anuncio: AnuncioAcessorioCreate
    estoque: EstoqueInfo


class AnuncioAcessorioResponseWithEstoque(BaseModel):
    anuncio: AnuncioAcessorioOut
    estoque: EstoqueOut


# ---------------------------
# PEÇAS
# ---------------------------

class AnuncioPecaCreate(BaseModel):
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    tipo_peca: Optional[str] = None
    marca: Optional[str] = None
    compatibilidade: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: Optional[str] = "ativo"


class AnuncioPecaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo_peca: Optional[str] = None
    marca: Optional[str] = None
    compatibilidade: Optional[str] = None
    condicao: Optional[str] = None
    preco: Optional[Decimal] = None
    status: Optional[str] = None

class AnuncioPecaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_pessoa: int
    titulo: str
    descricao: Optional[str] = None
    tipo_peca: Optional[str] = None
    marca: Optional[str] = None
    compatibilidade: Optional[str] = None
    condicao: Optional[str] = None
    preco: Decimal
    status: str
    created_at: datetime
    updated_at: datetime


class AnuncioPecaCreateWithEstoque(BaseModel):
    anuncio: AnuncioPecaCreate
    estoque: EstoqueInfo


class AnuncioPecaResponseWithEstoque(BaseModel):
    anuncio: AnuncioPecaOut
    estoque: EstoqueOut

from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


# --------- BIKES ---------

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


# --------- ACESSÓRIOS ---------

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


# --------- PEÇAS ---------

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

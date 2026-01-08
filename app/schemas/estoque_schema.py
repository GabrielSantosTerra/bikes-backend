from pydantic import BaseModel
from typing import Optional

from app.schemas.user_schema import UserResponse


class PessoaResponse(BaseModel):
    nome_completo: str
    cpf_cnpj: str
    email: str
    telefone_celular: Optional[str] = None
    data_nascimento: Optional[str] = None
    tipo_pessoa: str
    fantasia: Optional[str] = None
    regime: Optional[str] = None


class EstoqueInfo(BaseModel):
    quantidade: int = 0


class AnuncioRef(BaseModel):
    id_anuncio: int
    tipo_anuncio: str  # bikes | acessorios | pecas


class EstoqueCreateNested(BaseModel):
    anuncio: AnuncioRef
    estoque: EstoqueInfo


class EstoqueUpdateNested(BaseModel):
    estoque: EstoqueInfo


class EstoqueOut(BaseModel):
    id: int
    id_anuncio: int
    tipo_anuncio: str
    quantidade: int


class EstoqueResponseNested(BaseModel):
    pessoa: PessoaResponse
    usuario: Optional[UserResponse] = None
    estoque: EstoqueOut

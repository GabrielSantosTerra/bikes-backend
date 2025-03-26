from pydantic import BaseModel, EmailStr
from typing import Optional

class PessoaCreate(BaseModel):
    """Schema para cadastro na tabela pessoas"""
    nome_completo: str
    cpf_cnpj: str
    telefone_celular: Optional[str] = None
    telefone_fixo: Optional[str] = None
    email: EmailStr
    data_nascimento: Optional[str] = None

class UsuarioCreate(BaseModel):
    """Schema para cadastro na tabela usuarios"""
    email: EmailStr
    senha: str

class CadastroUsuario(BaseModel):
    """Schema que unifica cadastro de pessoas e usuários"""
    pessoa: PessoaCreate
    usuario: UsuarioCreate

class UserLogin(BaseModel):
    """Schema para login de usuários"""
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    """Schema para resposta de usuários autenticados"""
    nome: str
    cpf: str
    nascimento: Optional[str] = None
    telefone: Optional[str] = None
    email: EmailStr

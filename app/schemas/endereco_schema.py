from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: str | None = None
    bairro: str
    nome_cidade: str
    nome_estado: str
    endereco_primario: bool = False
class EnderecoUpdate(BaseModel):
    id: int
    cep: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    nome_cidade: str
    nome_estado: str
    endereco_primario: bool


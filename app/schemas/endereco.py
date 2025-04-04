from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: str | None = None
    bairro: str
    id_cidade: int

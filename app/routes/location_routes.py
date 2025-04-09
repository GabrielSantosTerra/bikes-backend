from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models.user_model import Usuario
from app.models.endereco_model import Endereco
from app.schemas.endereco_schema import EnderecoUpdate
from app.database.connection import get_db
from config.settings import settings

router = APIRouter()

@router.put("/endereco/update")
def update_endereco(
    dados: EnderecoUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    try:
        # 🔐 Valida token e encontra usuário
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Busca o endereço pelo ID e valida se pertence à pessoa
        endereco = db.query(Endereco).filter(
            Endereco.id == dados.id,
            Endereco.id_pessoa == user.id_pessoa
        ).first()

        if not endereco:
            raise HTTPException(status_code=404, detail="Endereço não encontrado ou não pertence ao usuário")

        if dados.endereco_primario:
            db.query(Endereco).filter(
                Endereco.id_pessoa == user.id_pessoa,
                Endereco.id != endereco.id
            ).update({Endereco.endereco_primario: False})

        endereco.cep = dados.cep
        endereco.logradouro = dados.logradouro
        endereco.numero = dados.numero
        endereco.complemento = dados.complemento
        endereco.bairro = dados.bairro
        endereco.nome_cidade = dados.nome_cidade
        endereco.nome_estado = dados.nome_estado
        endereco.endereco_primario = dados.endereco_primario

        db.commit()
        db.refresh(endereco)

        return {"message": "Endereço atualizado com sucesso"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@router.delete("/endereco/delete/{id}")
def deletar_endereco(id: int, request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        endereco = db.query(Endereco).filter(Endereco.id == id, Endereco.id_pessoa == user.id_pessoa).first()
        if not endereco:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")

        db.delete(endereco)
        db.commit()

        return {"message": "Endereço deletado com sucesso"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

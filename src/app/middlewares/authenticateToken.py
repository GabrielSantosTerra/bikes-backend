from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "minha_chave_secreta")
ALGORITHM = "HS256"

# Middleware para verificar o token de autenticação
async def authenticate_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Acesso negado, token não fornecido.")

    token = auth_header.split(" ")[1] if " " in auth_header else None

    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido.")

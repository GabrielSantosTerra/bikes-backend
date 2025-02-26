from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "minha_chave_secreta")
ALGORITHM = "HS256"

# Middleware para autenticação via Token JWT
async def authenticate(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    try:
        token = auth_header.split(" ")[1]  # Extrai o token do header
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload  # Armazena o payload no estado da requisição
    except (JWTError, IndexError):
        raise HTTPException(status_code=403, detail="Token inválido.")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from app.models.userModel import User
from app.config.database import SessionLocal
from datetime import datetime, timedelta
import os

# Configuração do JWT
SECRET_KEY = os.getenv("JWT_SECRET", "minha_chave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Criação do roteador
router = APIRouter()

# Configuração do bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔍 Listar todos os usuários
@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar usuários: {error}")

# 📥 Registrar novo usuário
@router.post("/register")
async def register_user(user_data: dict, db: Session = Depends(get_db)):
    try:
        name = user_data.get("name")
        email = user_data.get("email")
        password = user_data.get("password")
        cpf = user_data.get("cpf")
        birth_date = user_data.get("birth_date")
        phone = user_data.get("phone")

        if not all([name, email, password, cpf, birth_date, phone]):
            raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios!")

        # Verificar se o e-mail ou CPF já existe
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado!")
        
        if db.query(User).filter(User.cpf == cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado!")

        # Criptografar a senha
        hashed_password = pwd_context.hash(password)

        # Criar novo usuário
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            cpf=cpf,
            birth_date=birth_date,
            phone=phone,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Usuário criado com sucesso!", "user": {"name": new_user.name, "email": new_user.email}}

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {error}")

# 🔑 Login do usuário
@router.post("/login")
async def login_user(credentials: dict, db: Session = Depends(get_db)):
    try:
        email = credentials.get("email")
        password = credentials.get("password")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Os campos email e senha são obrigatórios!")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado!")

        if not pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Credenciais inválidas!")

        # Geração do token JWT
        token_data = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "message": "Login bem-sucedido!",
            "token": token,
            "user": {"name": user.name, "email": user.email},
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar login: {error}")

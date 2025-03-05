from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.auth.security import get_password_hash, verify_password, create_access_token
from config.settings import settings
from app.utils.email_service import send_reset_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

def create_reset_token(user_id: int):
    """Gera um token de redefinição de senha com expiração"""
    expire = datetime.utcnow() + timedelta(minutes=30)  # Token válido por 30 min
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_reset_token(token: str):
    """Verifica e decodifica o token de redefinição de senha"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        exp: datetime = datetime.utcfromtimestamp(payload.get("exp"))

        if user_id is None or datetime.utcnow() > exp:
            return None
        return int(user_id)
    except JWTError:
        return None

@router.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado!")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        hashed_password=hashed_password,
        cpf=user.cpf,
        birth_date=user.birth_date,
        phone=user.phone,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário criado com sucesso"}

@router.post("/auth/login")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user_auth = db.query(User).filter(User.email == user.email).first()
    if not user_auth or not verify_password(user.password, user_auth.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": user_auth.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": user_auth.id, "name": user_auth.name, "email": user_auth.email}}

@router.post("/auth/logout")
def logout(response: Response, token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Remove o cookie do token
        response.delete_cookie("authToken")
        return {"message": "Logout realizado com sucesso"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

@router.get("/users/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Busca informações do usuário autenticado"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@router.post("/auth/request-password-reset")
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Gera e envia um token de redefinição de senha para o email do usuário"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    reset_token = create_reset_token(user.id)  # Gerar o token
    await send_reset_email(user.email, reset_token)  # Enviar e-mail

    return {"message": "Código de verificação enviado para o e-mail"}

@router.post("/auth/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    user_id = verify_reset_token(request.token)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.hashed_password = get_password_hash(request.new_password)
    db.commit()

    return {"message": "Senha redefinida com sucesso"}


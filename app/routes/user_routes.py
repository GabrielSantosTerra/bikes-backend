from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr

from app.database.connection import get_db
from app.models.user import Usuario, Pessoa
from app.schemas.user import PessoaCreate, UserLogin, UserResponse, CadastroUsuario
from app.auth.security import get_password_hash, verify_password, create_access_token
from config.settings import settings
from app.utils.email_service import send_reset_email
from passlib.context import CryptContext

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUpdate(BaseModel):
    nome: str
    email: str
    telefone: str
    cpf: str
    nascimento: str
    senha: str | None = None  # Senha é opcional

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    nova_senha: str

class PessoaCreate(BaseModel):
    nome_completo: str
    fantasia: str
    cpf_cnpj: str
    email: EmailStr
    telefone_celular: str
    data_nascimento: str
    regime: str
    tipo_pessoa:str

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str

class CadastroUsuario(BaseModel):
    pessoa: PessoaCreate
    usuario: UsuarioCreate

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

@router.post("/users/")
def criar_usuario(dados: CadastroUsuario, db: Session = Depends(get_db)):
    # Verificar se o email já existe na tabela de usuários
    if db.query(Usuario).filter(Usuario.email == dados.usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Extrai os dados da pessoa e define tipo_pessoa com base no tamanho do cpf_cnpj
    pessoa_data = dados.pessoa.dict()
    pessoa_data["tipo_pessoa"] = "PF" if len(pessoa_data["cpf_cnpj"]) <= 11 else "PJ"

    # Cria a nova pessoa
    nova_pessoa = Pessoa(**pessoa_data)
    db.add(nova_pessoa)
    db.commit()
    db.refresh(nova_pessoa)

    # Cria o usuário vinculado
    novo_usuario = Usuario(
        id_pessoa=nova_pessoa.id,
        email=dados.usuario.email,
        senha=get_password_hash(dados.usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "message": "Usuário cadastrado com sucesso",
        "id_pessoa": nova_pessoa.id,
        "id_usuario": novo_usuario.id
    }

@router.post("/auth/login/")
def login(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if not user or not verify_password(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token_expires = timedelta(minutes=60)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    # Criar a resposta JSON + adicionar o cookie
    response = JSONResponse(content={"message": "Login com sucesso", "id_usuario": user.id})
    response.set_cookie(
        key="authToken",
        value=token,
        httponly=True,
        secure=False,  # True apenas em produção HTTPS
        samesite="Lax",
        max_age=3600,
        path="/"
    )
    return response

@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("authToken")
    return {"message": "Logout realizado com sucesso"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("authToken")
    print("🍪 COOKIE RECEBIDO:", token)

    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        pessoa = db.query(Pessoa).filter(Pessoa.id == user.id_pessoa).first()
        if not pessoa:
            raise HTTPException(status_code=404, detail="Dados da pessoa não encontrados")

        return UserResponse(
            nome=pessoa.nome_completo,
            cpf=pessoa.cpf_cnpj,
            nascimento=pessoa.data_nascimento,
            telefone=pessoa.telefone_celular,
            email=pessoa.email
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@router.post("/auth/request-password-reset")
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Envia token de redefinição de senha por e-mail"""
    user = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    reset_token = create_reset_token(user.id)  # Gerar o token
    await send_reset_email(user.email, reset_token)  # Enviar e-mail

    return {"message": "Código de verificação enviado para o e-mail"}

@router.post("/auth/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Redefine a senha do usuário"""
    user_id = verify_reset_token(request.token)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")

    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.senha = get_password_hash(request.nova_senha)
    db.commit()

    return {"message": "Senha redefinida com sucesso"}

@router.put("/users/update", response_model=UserResponse)
def update_user(
    user_data: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Atualiza dados do usuário e sincroniza com a tabela de pessoas"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")

        user = db.query(Usuario).filter(Usuario.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Buscar pessoa vinculada ao usuário
        pessoa = db.query(Pessoa).filter(Pessoa.id == user.id_pessoa).first()
        if not pessoa:
            raise HTTPException(status_code=404, detail="Dados da pessoa não encontrados")

        # Atualiza os dados do usuário e da pessoa
        user.email = user_data.email
        pessoa.email = user_data.email
        user.telefone = user_data.telefone
        pessoa.telefone_celular = user_data.telefone
        user.cpf = user_data.cpf
        pessoa.cpf_cnpj = user_data.cpf
        user.nascimento = user_data.nascimento
        pessoa.data_nascimento = user_data.nascimento
        user.nome = user_data.nome
        pessoa.nome_completo = user_data.nome

        if user_data.senha:
            user.senha = get_password_hash(user_data.senha)

        db.commit()
        db.refresh(user)
        db.refresh(pessoa)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

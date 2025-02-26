from passlib.context import CryptContext

# Configuração do bcrypt para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar o hash da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

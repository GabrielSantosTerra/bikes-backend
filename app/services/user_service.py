from sqlalchemy.orm import Session
from app.models.user import User, Pessoa
from app.auth.security import get_password_hash
from app.schemas.user import UserResponse  # Import UserResponse

def create_user_and_person(db: Session, nome: str, fantasia: str, cpf_cnpj: str, email: str, telefone: str, senha: str, nascimento: str, regime:str):
    hashed_password = get_password_hash(senha)

    # Verifica se já existe CPF ou E-mail cadastrado
    if db.query(User).filter(User.cpf == cpf_cnpj).first() or db.query(User).filter(User.email == email).first():
        return None

    nova_pessoa = Pessoa(
        nome_completo=nome,
        fantasia=fantasia,
        cpf_cnpj=cpf_cnpj,
        email=email,
        telefone_celular=telefone,
        data_nascimento=nascimento,
        regime=regime,
        tipo_pessoa="PF"  # Para usuários comuns, será sempre 'PF'

    )

    db.add(nova_pessoa)
    db.commit()
    db.refresh(nova_pessoa)

    novo_usuario = User(
        nome=nome,
        senha=hashed_password,
        cpf=cpf_cnpj,
        nascimento=nascimento,
        telefone=telefone,
        email=email,
        id_pessoa=nova_pessoa.id
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return UserResponse(
        nome=novo_usuario.nome,
        cpf=novo_usuario.cpf,
        nascimento=novo_usuario.nascimento,
        telefone=novo_usuario.telefone,
        email=novo_usuario.email
    )

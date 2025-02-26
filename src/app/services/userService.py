from sqlalchemy.orm import Session
from app.models.userModel import User

# Serviço para obter todos os usuários
def get_users(db: Session):
    return db.query(User).all()

# Serviço para criar um novo usuário
def create_user(db: Session, data: dict):
    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

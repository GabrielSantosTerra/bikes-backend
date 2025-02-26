from sqlalchemy import create_engine
from main import Base, engine

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)
print("Banco de dados atualizado com sucesso!")

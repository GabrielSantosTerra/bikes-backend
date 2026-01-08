from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.settings import settings

# print(f"Conectando ao banco: {settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para testar a conexão com o banco de dados
def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexão estabelecida com sucesso ao banco de dados!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

# Chama a função de teste ao carregar o módulo
test_connection()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DB_NAME = os.getenv("DB_NAME", "bikes_dev")
DB_USER = os.getenv("DB_USER", "bikes_dev")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Tsc10012000@")
DB_HOST = os.getenv("DB_HOST", "bikes_dev.postgresql.dbaas.com.br")
DB_PORT = os.getenv("DB_PORT", "5432")  # Porta padrão do PostgreSQL

# String de Conexão
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criação da Engine e Sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Testar Conexão
def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexão com o banco de dados bem-sucedida! 🚀")
    except Exception as error:
        print(f"Erro ao conectar ao banco: {error}")

# Teste ao importar o módulo
test_connection()

from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.database.connection import Base, engine
import app.models.user  # Import necessário para garantir a criação das tabelas
from fastapi.middleware.cors import CORSMiddleware

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar a instância do FastAPI
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(user_router)
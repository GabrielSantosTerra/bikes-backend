from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.ibge_routes import router as localidades_router
from app.routes.location_routes import router as endereco_router
from app.database.connection import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(__file__))

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar a instância do FastAPI
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou domínio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir rotas
app.include_router(user_router)
app.include_router(localidades_router)
app.include_router(endereco_router)

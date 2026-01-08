from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

from app.routes.user_routes import router as user_router
from app.routes.ibge_routes import router as ibge_router
from app.routes.endereco_routes import router as endereco_router
from app.database.connection import Base, engine
from app.routes.anuncio_bikes_routes import router as anuncio_bikes_router
from app.routes.anuncio_acessorios_routes import router as anuncio_acessorios_router
from app.routes.anuncio_pecas_routes import router as anuncio_pecas_router

sys.path.append(os.path.dirname(__file__))

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar a instância do FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou domínio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir rotas
app.include_router(user_router)
app.include_router(ibge_router)
app.include_router(endereco_router)
app.include_router(anuncio_bikes_router)
app.include_router(anuncio_acessorios_router)
app.include_router(anuncio_pecas_router)
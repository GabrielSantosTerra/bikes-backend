from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.userRoute import user_route

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(user_route.router, prefix="/users")

@app.get("/")
async def root():
    return {"message": "Servidor em execução 🚀"}

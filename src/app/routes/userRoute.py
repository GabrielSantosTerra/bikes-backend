from fastapi import APIRouter, Depends, Request
from app.controllers.userController import get_all_users
from app.middlewares.authenticate import authenticate

router = APIRouter()

@router.get("/protected")
async def protected_route(request: Request, _=Depends(authenticate)):
    user = request.state.user
    return {"message": f"Acesso concedido para {user['email']}!"}

@router.get("/")
async def public_route():
    return {"message": "Esta rota é pública!"}

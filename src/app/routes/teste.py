from fastapi import APIRouter

router = APIRouter()

@router.get("/message")
async def get_message():
    return {
        "message": "Bem-vindo ao Bikes.com!",
        "status": "success"
    }

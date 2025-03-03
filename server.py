import uvicorn
from main import app
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

PORT = int(os.getenv("PORT", 3000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)

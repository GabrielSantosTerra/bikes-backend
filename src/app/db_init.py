from app.config.database import engine
from app.models.userModel import Base

# Criar todas as tabelas definidas nos modelos
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")

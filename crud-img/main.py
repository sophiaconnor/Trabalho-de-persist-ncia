from fastapi import FastAPI
from routes import fotos
from core.logging_config import logger

app = FastAPI(
    title="QXD0099 - API Acervo de fotos",
    description=(
        "API de persistência de fotos, com operações CRUD (Create, Read, Update, Delete) para gerenciar o acervo de fotos."
    ),
    version="1.0.0")

#app.include_router(fotos.router, prefix="/fotos", tags=["fotos"])
app.include_router(fotos.router)
@app.get("/", tags=["Sistema"])
def home():
    logger.info("Endpoint raiz acessado.")

    return {
        "mensagem": "API de Acervo de Fotos - Persistência",
        "recursos": [
            "/fotos",
        ],
    }

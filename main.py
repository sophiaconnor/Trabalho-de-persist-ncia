from fastapi import FastAPI

from routes.fotos import router as fotos_router
from core.logging_config import logger


app = FastAPI(
    title="Acervo de Fotos API",
    description=(
        "API didática com FastAPI, persistência em JSON, "
        "exportação para CSV e logging configurado por YAML."
    ),
    version="1.0.0",
)

app.include_router(fotos_router)


@app.get("/", tags=["Sistema"])
def home():
    logger.info("Endpoint raiz acessado.")

    return {
        "mensagem": "Acervo de Fotos - Persistência em JSON",
        "recursos": [
            "/fotos",
            "/docs",
            "/redoc",
        ],
    }
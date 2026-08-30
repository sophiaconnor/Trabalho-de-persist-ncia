from fastapi import FastAPI
from app.services.backup_service import executar_backup
from app.routes.backup import router as backup_router

app = FastAPI()
app.include_router(backup_router)

@app.post("/backup")
def fazer_backup():
    
    resultado = executar_backup()

    if resultado is None:
        return {
            "mensagem": "O backup já existe."
        }

    return {
        "mensagem": "Backup realizado com sucesso.",
        "arquivo": resultado
    }
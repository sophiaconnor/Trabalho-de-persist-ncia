from fastapi import FastAPI
from app.services.backup_service import executar_backup
from app.routes.backup import router as backup_router

# Cria uma instância do FastAPI
app = FastAPI()
# Inclui o roteador de backup na aplicação FastAPI
app.include_router(backup_router)

@app.post("/backup")
def fazer_backup():

    #executar o backup chamando a função executar_backup
    resultado = executar_backup()

    #checa se o resultado é None, indicando que o backup já existe
    if resultado is None:
        return {
            "mensagem": "O backup já existe."
        }

    #retorna uma mensagem de sucesso e o caminho do arquivo de backup criado
    return {
        "mensagem": "Backup realizado com sucesso.",
        "arquivo": resultado
    }
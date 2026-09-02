from fastapi import APIRouter
from app.services.backup_service import executar_backup
from app.services.backup_service import obter_backups

# Definir o roteador para a rota de backup
router = APIRouter()


@router.post("/backup")
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

@router.get("/backups")
def listar_backups_api():
    #retorna a lista de arquivos de backup encontrados
    backups = obter_backups()
    #retorna a lista de arquivos de backup encontrados
    return {
        "backups": backups
    }
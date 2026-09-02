from app.services.backup import criar_backup
from app.services.backup import criar_backup, listar_backups
# Função para executar o backup chamando a função criar_backup
def executar_backup():
    return criar_backup()

# Função para listar os arquivos de backup existentes
def obter_backups():
    return listar_backups()
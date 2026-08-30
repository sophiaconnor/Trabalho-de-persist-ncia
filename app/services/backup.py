import zipfile
import os
from datetime import datetime

#define o nome do arquivo de backup com base na data e hora atual
agora = datetime.now()
data_hora = agora.strftime("%d-%m-%Y_%H%M")
nome_backup = f"backup_{data_hora}.zip"

#define o caminho da pasta que será compactada
local_da_pasta = r'C:\Users\sophi\OneDrive\Documentos\Trabalho-de-persist-ncia\storage\files'

#define o caminho de destino do arquivo compactado
destino_da_compactacao =  os.path.join(r'C:\Users\sophi\OneDrive\Documentos\Trabalho-de-persist-ncia\storage\backups', nome_backup)


pastas_para_backup = [
    r'C:\Users\sophi\OneDrive\Documentos\Trabalho-de-persist-ncia\storage\files',
    r'C:\Users\sophi\OneDrive\Documentos\Trabalho-de-persist-ncia\storage\metadata'
]

#verifica se o arquivo de backup já existe antes de criar um novo
if not os.path.exists(destino_da_compactacao):
    #realiza a compactação da pasta
    with zipfile.ZipFile(
        destino_da_compactacao,
        'w',
        zipfile.ZIP_DEFLATED
    ) as zipf:
        for root, subFolders, files in os.walk(local_da_pasta):
            for file in pastas_para_backup:
                caminho_completo = os.path.join(root, file)
                zipf.write(caminho_completo, os.path.relpath(caminho_completo, local_da_pasta))

    #avisa que o backup foi realizado com sucesso e informa o caminho do arquivo de backup criado
    print(f"Backup realizado com sucesso! Arquivo de backup criado: {destino_da_compactacao}")

#avisa se o arquivo de backup já existe
else:
    print(f"O arquivo de backup {nome_backup} já existe.")


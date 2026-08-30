import zipfile
import os
from datetime import datetime

def criar_backup():

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
    pasta_storage = r'C:\Users\sophi\OneDrive\Documentos\Trabalho-de-persist-ncia\storage'

    #verifica se o arquivo de backup já existe antes de criar um novo
    if not os.path.exists(destino_da_compactacao):
        #realiza a compactação da pasta
        with zipfile.ZipFile(
            destino_da_compactacao,
            'w',
            zipfile.ZIP_DEFLATED
        ) as zipf:
            for pasta in pastas_para_backup:
                for root, subFolders, files in os.walk(pasta):
                    for file in files:
                        caminho_completo = os.path.join(root, file)
                        #print("Adicionando ao ZIP:", caminho_completo)
                        zipf.write(
                            caminho_completo,
                            os.path.relpath(caminho_completo, pasta_storage)
                        )

        #avisa que o backup foi realizado com sucesso e informa o caminho do arquivo de backup criado
        #print(f"Backup realizado com sucesso! Arquivo de backup criado: {destino_da_compactacao}")

    return destino_da_compactacao
from zipfile import ZipFile
# Criar um arquivo ZIP
with ZipFile('arquivo.zip', 'w') as zipf:
    zipf.write('arquivo1.txt') # Substitua pelo caminho do arquivo
    zipf.write('arquivo2.txt') # Substitua pelo caminho do arquivo
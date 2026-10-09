# Trabalho-de-persist-ncia
nome do projeto: 
API de Acervo de Fotos

integrantes: 
Ana Vitória de Melo Silva
Anna Rayca Alves Cardoso
Sophia Muniz de Oliveira

tema recebido: 
Acervo Fotográfico Institucional

objetivo: 
Armazenar fotografias e outros arquivos relacionados ao registro de atividades institucionais.


requisitos:
1. armazenamento de arquivos:
O sistema deve permitir realizar o upload e armazenar fisicamente o arquivo enviado.
2. Listagem de documentos:
O sistema deve permitir a listagem de todos os documentos armazenados no sistema, retornando seus respectivos metadados.
3. Consulta de documentos:
O sistema deve permitir a consulta de um documento por meio de seu ID, retornando seus respectivos metadados. Caso o documento não exista, deverá ser retornada uma resposta HTTP adequada.
4. Download do arquivo:
O sistema deve permitir recuperar o arquivo armazenado pelo sistema.
5. Atualização de metadados:
O sistema deve permitir atualização dos metadados do documento. 
6. Exclusão de documentos:
O sistema deve permitir excluir documentos por meio do ID, removendo também o arquivo físico correspondente.
7. Filtragem de documentos:
O sistema deve permitir a realização de consultas utilizando pelo menos três critérios diferentes.
8. Estatísticas e análise do Acervo Fotográfico:
O sistema deve apresentar estatísticas do acervo utilizando os dados efetivamente persistidos, incluindo, no mínimo, a quantidade total de documentos, o tamanho total ocupado, a quantidade de documentos por extensão, por categoria, por evento, por ano e por formato da imagem.
9.  Exportação para CSV:
O sistema deve permitir a geração de um arquivo CSV contendo o catálogo atual dos documentos armazenados e seus respectivos metadados.
10. Verificação de integridade:
O sistema deve permitir verificar a integridade de um arquivo armazenado.
11. Backup dos dados:
O sistema deve permitir a geração de backups contendo os arquivos armazenados e seus respectivos metadados.
12. Registro de operações:
O sistema deve registrar em arquivo de log as principais operações realizadas no sistema, incluindo upload, download, consulta, atualização, exclusão, backup e verificação de integridade.
13. Configuração externa:
O sistema deve utilizar um arquivo externo de configuração para definir parâmetros como diretórios de armazenamento, limite de upload e nível de log.
14. Tratamento de erros:
O sistema deve tratar erros relacionados a arquivos, JSON, configurações, upload, backup e operações com documentos, retornando mensagens e códigos HTTP adequados quando aplicável.

bibliotecas utilizadas:
fastapi
uvicorn
pandas

instruções de instalação:
pip install fastapi uvicorn 
pip install pandas

instruções de execução:
no terminal, executar as seguintes instruções:
1. para entrar na pasta do crud: cd crud-img
2. python -m uvicorn app.main:app --reload
2. (acessar) http://127.0.0.1:8000

descrição da estrutura do projeto:
Trabalho-de-persistencia/
    app/
        models/ #talvez apagar depois
        routes/
        services/
        utils/
        main.py #talvez apagar depois

    config/ #talvez apagar depois
        gitkeep

    crud-img/
        core/
        data/
        models/
        routes/
        services/

── storage/
        backups/
        exports/ #talvez apagar depois
        files/
        logs/
        metadata/

── .gitignore
── README.md

principais endpoints:
## Principais endpoints

Fotos

Método: GET
Endpoint: `/fotos/`
Descrição: Lista as fotos cadastradas

Método: POST
Endpoint: `/fotos/`
Descrição: Cadastra uma nova foto

Método: GET
Endpoint: `/fotos/csv`
Descrição: Lista os dados das fotos em CSV

Método: PUT
Endpoint: `/fotos/{foto_id}`
Descrição: Atualiza os dados de uma foto

Método: DELETE
Endpoint: `/fotos/{foto_id}`
Descrição: Remove uma foto

Backups

Método: POST
Endpoint: `/backup`
Descrição: Realiza um backup compactado dos dados

Método: GET
Endpoint: `/backups`
Descrição: Lista os backups disponíveis

exemplos de utilização:
Para cadastrar uma foto, o usuário realiza uma requisição POST /fotos/, enviando o arquivo e informações como categoria e descrição.
Para atualizar os dados de uma foto cadastrada, o usuário realiza uma requisição PUT /fotos/{foto_id}, informando o ID da foto e os novos valores para categoria e/ou descrição.
Para excluir uma foto cadastrada, o usuário realiza uma requisição DELETE /fotos/{foto_id}, informando o ID correspondente à foto que deseja remover.
Para consultar as fotos cadastradas, o usuário realiza uma requisição GET /fotos/. A API retorna os registros das fotos armazenadas, incluindo seus metadados.

metadados específicos do domínio:
01: autor (fotógrafo)
02. nome_original
03. nome_armazenado
04. extensao
07. categoria 
08. descricao 
09. ano
10. local


descrição da funcionalidade específica do tema: retorna um agrupamento feito por meio de uma análise da lista de fotos e gera estatísticas sobre a mesma com os atributos de evento, ano e formato do arquivo.

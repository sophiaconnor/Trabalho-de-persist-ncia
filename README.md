# Trabalho-de-persist-ncia
nome do projeto: 

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
O sistema deve permitir a listagem de todos os documentos armazenados no sistema, , retornando seus respectivos metadados.
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

instruções de instalação:

instruções de execução:

descrição da estrutura do projeto:

principais endpoints:

exemplos de utilização:

metadados específicos do domínio:

descrição da funcionalidade específica do tema:

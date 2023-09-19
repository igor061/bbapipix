# bbapipix

1. Para usar a api do cconsulta de pix do BB é preciso se cadastrar no site: https://www.bb.com.br/site/developers/
    Obs: Tem que ser o CPF do representatnte da empresa. Ele pode dar acesso a outros CPFs.
2. Criar um uma aplicacao com acesso a API PIX v2. (NOVA APLICAÇÃO)
3. Gerar um certificado no menu CERTIFICADOS / CERTIFICADOS BB
   Obs.: Nao precisa enviar o certificado, só se for usar um ICP Brasil
          Salvar os arquivos de cahve e certificado.
          Colocar o conteudo dos dois arquivos em um unico arquivo
          Salvar na pasta do projeto, exemplo 'client_certs/'
4. Enviar a aplicação para producao
5. Guardar as credenciais (em CREDENCIAS) dos dois ambientes Testes e Produção
     - developer_application_key
     - client_id
     - client_secret
6. No arquivo bbapipix/consulta_pix.py tem um exemplo de como usar
7. Se precisar pegar os certificados atualizados dos servidores, tem em bbapipix/utils/getserver_certificate.py uma
script que pega a cadeis atual direto dos servidores. Ela precisa do openssl instalado.
Será preciso pegar de todos e no env.py definir a variável PATH_SERVER_CERTS para o diretorio que vc salvar os certificados.
O nome do aquivo deve ser o endereco do servidor com a extensao.cer. Exemplo: api-pix.hm.bb.com.br.cer
   
8. criar um arquivo env.py no raiz do projeto com as seguintes informações de cada empresa:

~~~python
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

credenciais = {
    'empresa': {
        "developer_key":  "45c37a21cdaasdfasdfasf434d1ee2",
        "client_id": "eyJpZCI6IjQ3ODBhMjasfdasfasfasdfasdfasdfasfasfassdfasfsfafsaAtNmM2Mi00Nzk5LTk3OWEiLCJjasdfasdfasfdasfdWxJbnN0YWxhY2FvIjoxfQ",
        "client_secret": "eyJpZCI6ImNmYjc3ZDgtYzFkYy00MDhiLasdfasdfasdfasfdasdfasdfasdfasdfasdffasdfasdfafsdafcmUiOjU0NDMxLCJzZXF1ZW5jaWFsSW5zdGFsYWNhbyI6MSwic2VxdWVuY2lhbENyZWRlbmNpYWwiOjEsImFtYmllbnRlIjoicHJvZHVjYW8iLCJpYXQiOjE2OTQ4NDY0NTEzMDd9",
        "client_certificate": "bb-empresa-20230918.pem",
        'enviroment': "PROD",
    },

    'homolog_empresa': {
        "developer_key": "799fasdfasdfasdfasdfasdfasd35594789",
        "client_id": "eyJpZCI6ImUzIiwiY29fasdfasdfasdfasdfasdfasdfasdfas0MTIwLCJzZXF1ZW5jaWFsSW5zdGFsYWNhbyI6MX0",
        "client_secret": "eyJpZCI6IiIsImdasdfasdfasdfasdfasdfasfdasdfasdfasdfasfasdfsInNlcXVlbmNpYWxDcmVkZW5jaWFsIjoxLCJhbWJpZW50ZSI6ImhvbW9sb2dhY2FvIiwiaWF0IjoxNjk0ODEyODAyNzI1fQ",
        "client_certificate": "bb-empresa-20230918.pem",
        'enviroment': "STAGE",
    }
}

#PATH_SERVER_CERTS = PATH_BBPIXLIB+'server_certs/'
PATH_CLIENT_CERTS = PROJECT_PATH+'/client_certs/'
~~~


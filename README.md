# bbapipix - Configuração e Uso da API de Consulta Pix do Banco do Brasil

1. **Cadastro no Portal de Desenvolvedores BB:**
   - Para começar, é necessário se cadastrar no site [Portal de Desenvolvedores BB](https://www.bb.com.br/site/developers/).
   - O cadastro deve ser feito com o CPF do representante da empresa, que terá a capacidade de conceder acesso a outros CPFs.

2. **Criação de uma Nova Aplicação:** 
   - No portal, crie uma nova aplicação com acesso à API Pix V2. Certifique-se de selecionar a opção "Nova Aplicação".

3. **Geração de Certificado:**
   - No menu "CERTIFICADOS" no portal, gere um certificado.
   - Lembre-se de que você não precisa enviar o certificado, a menos que esteja usando um certificado ICP Brasil.
   - Salve os arquivos de chave e certificado.
   - Coloque o conteúdo dos dois arquivos em um único arquivo e salve-o na pasta do seu projeto, por exemplo, 'client_certs/'.

4. **Envio da Aplicação para Produção:**
   - Siga os procedimentos do portal para enviar a sua aplicação para o ambiente de produção.

5. **Guardar Credenciais:** 
   - No portal, na seção "CREDENCIAIS", obtenha as seguintes credenciais para os ambientes de testes e produção:
     - developer_application_key
     - client_id
     - client_secret

6. **Exemplo de Uso:** 
   - No arquivo `bbapipix/consulta_pix.py`, você encontrará um exemplo de como usar a API de consulta Pix.

7. **Obtenção de Certificados Atualizados:**
   - Se você precisar obter os certificados atualizados dos servidores, utilize o script `bbapipix/utils/getserver_certificate.py`.
   - Certifique-se de ter o OpenSSL instalado.
   - Você precisará obter os certificados de todos os servidores e definir a variável `PATH_SERVER_CERTS` no arquivo `env.py` para o diretório onde você os salvou.
   - Os nomes dos arquivos devem ser o endereço do servidor com a extensão `.cer`. Por exemplo:
     `api-pix.hm.bb.com.br.cer`.

8. **Configuração do Arquivo `env.py`:**
   - Crie um arquivo `env.py` na raiz do seu projeto com as informações de cada empresa. Um exemplo de configuração está abaixo:

```python
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
        "client_id": "eyJpZCI6ImUzIwiY29fasdfasdfasdfasdfasdfasdfasdfas0MTIwLCJzZXF1ZW5jaWFsSW5zdGFsYWNhbyI6MX0",
        "client_secret": "eyJpZCI6IiIsImdasdfasdfasdfasdfasdfasfdasdfasdfasdfasfasdfsInNlcXVlbmNpYWxDcmVkZW5jaWFsIjoxLCJhbWJpZW50ZSI6ImhvbW9sb2dhY2FvIiwiaWF0IjoxNjk0ODEyODAyNzI1fQ",
        "client_certificate": "bb-empresa-20230918.pem",
        'enviroment': "STAGE",
    }
}

#PATH_SERVER_CERTS = PATH_BBPIXLIB+'server_certs/'
PATH_CLIENT_CERTS = PROJECT_PATH+'/client_certs/'
```

Certifique-se de ajustar as informações de acordo com o ambiente e as credenciais específicas de sua empresa. Essas configurações permitirão que você utilize a API de consulta Pix do Banco do Brasil em seu projeto.

# prod_srgold
import json

import env
from bbapilib_v2 import BBClient, BBClientSandbox


def pega_lista_pix(credentials, dthr_ini, dthr_fim):

    client = BBClient.from_credentials(
        **credentials
    )

    resp = client.received_pixs(dthr_ini, dthr_fim)

    #print(resp.json())
    return resp.json()


def trata_resp_pix(json_resp):
    #pprint(resp_json['pix'])
    dados_pix = []
    for pix in json_resp['pix']:
        dados = {
            'valor': pix['componentesValor']['original']['valor'],
            'horario': pix['horario'],
            'id': pix['endToEndId'],
            'msg': pix['txid'],
            'devolucoes': pix['devolucoes']
        }
        pagador = pix['pagador']
        dados['cpf/cnpj'] = pagador.get('cnpj', pagador.get('cpf'))
        dados['nome'] = pagador.get('nome')

        dados_pix.append(dados)
        #print(dados)
    return dados_pix


def consuta_pix(key_credentials, dthr_ini, dthr_fim):
    credentials = env.credenciais[key_credentials]
    resp_json = pega_lista_pix(credentials, dthr_ini, dthr_fim)
    dados = trata_resp_pix(resp_json)
    return dados


if __name__ == '__main__':
    from pprint import pprint


    def teste01():
        dthr_ini = '2023-09-01T00:00:01Z'
        dthr_fim = "2023-09-05T23:59:59Z"
        #key_credentials = 'homolog_srgold'
        key_credentials = 'srgold'

        dados = consuta_pix(key_credentials, dthr_ini, dthr_fim)

        pprint(dados)

    teste01()
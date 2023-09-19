from datetime import datetime, timedelta

import requests
from requests.auth import AuthBase

import env


class BadCredentials(Exception):
    ...


class EmptyPixList(Exception):
    ...


PATH_SERVER_CERTS = env.PATH_SERVER_CERTS
PATH_CLIENT_CERTS = env.PATH_SERVER_CERTS
SERVERS_CONF = {
    'PROD': {
        'auth': {
            'endpoint': 'https://oauth.bb.com.br/oauth/token',
            'server_cert': 'oauth.bb.com.br.cer',
        },
        'api': {
            'endpoint': 'https://api-pix.bb.com.br/pix/v2/',
            'server_cert': 'api-pix.bb.com.br.cer',
        },
    },

    'STAGE': {
        'auth': {
            'endpoint': 'https://oauth.sandbox.bb.com.br/oauth/token',
            'server_cert': 'oauth.sandbox.bb.com.br.cer',
        },
        'api': {
            'endpoint': 'https://api-pix.hm.bb.com.br/pix/v2/',
            'server_cert': 'api-pix.hm.bb.com.br.cer',
        }
    }
}


class BBAuth(AuthBase):

    def __init__(self, client_id, client_secret, developer_key, client_certificate, endpoint, server_cert):
        self.credentials = (client_id, client_secret)
        self.certificate = env.PATH_CLIENT_CERTS + client_certificate
        self.developer_key = developer_key
        self._token = None
        self.expires_in = None

        self.endpoint = endpoint
        self.cert = PATH_SERVER_CERTS + server_cert

    @property
    def is_valid(self):
        now = datetime.now()
        if not self._token or not self.expires_in or self.expires_in <= now:
            return False
        return True

    @property
    def token(self):
        if not self.is_valid:
            self.renew()
        return self._token

    @token.setter
    def token(self, token):
        type_, value = token
        self._token = f'{type_} {value}'

    def handle_401(self, r, **kwargs):
        if r.status_code != 401:
            return r

        # force token renew
        self.renew()

        # Consume content and release the original connection
        # to allow our new request to reuse the same one.
        r.content
        r.close()
        prep = r.request.copy()

        prep.headers['Authorization'] = self.token
        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep

        return _r

    def renew(self):
        data = {
            'grant_type': 'client_credentials',
            'code': self.developer_key,
        }

        resp = requests.post(self.endpoint, data=data, verify=self.cert, auth=self.credentials)
        if resp.status_code == 401:
            raise BadCredentials()

        if resp.status_code == 400:
            raise RuntimeError(resp.json())

        json = resp.json()
        self.token = json['token_type'], json['access_token']

        self.expires_in = datetime.now() + timedelta(seconds=json['expires_in'])

    def __call__(self, r):
        r.headers['Authorization'] = self.token
        r.headers['x-developer-application-key'] = self.developer_key
        r.register_hook("response", self.handle_401)
        return r


class BBSession(requests.Session):

    def __init__(self, auth, endpoint, server_cert):
        super().__init__()
        self.auth = auth
        self.endpoint = endpoint
        self.server_cert = PATH_SERVER_CERTS + server_cert

    def request(self, method: str, path='', *args, **kwargs):
        url = self.endpoint + path
        # print(url)
        resp = super().request(method, url, *args, cert=self.auth.certificate, verify=self.server_cert, **kwargs)
        return resp


class BBClient:
    AUTH = BBAuth
    SESSION = BBSession

    def __init__(self, session):
        self.session = session

    @classmethod
    def from_credentials(cls, client_id: str,
                         client_secret: str, developer_key: str, client_certificate: str, enviroment: str):
        server_auth = SERVERS_CONF[enviroment]['auth']
        auth = cls.AUTH(client_id, client_secret, developer_key, client_certificate, **server_auth)
        server_api = SERVERS_CONF[enviroment]['api']
        session = cls.SESSION(auth, **server_api)
        return cls(session)

    def request(self, method, path='', params=None, data=None, *args, **kwargs):
        resp = self.session.request(method, path=path, params=params, data=data, *args, **kwargs)
        if resp.status_code == 404:
            raise EmptyPixList

        resp.raise_for_status()
        return resp

    # init_datetime: '2023-09-01T00:00:01UTC-3'
    def received_pixs(self, init_datetime, end_datetime):
        params = {
            'inicio': init_datetime,
            'fim': end_datetime
        }

        resp = self.request('get', path='/pix', params=params)

        return resp

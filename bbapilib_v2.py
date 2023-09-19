from datetime import datetime, timedelta

import requests
from requests.auth import AuthBase

import env


class BadCredentials(Exception):
    ...


class BBAuth(AuthBase):
    OAUTH_ENDPOINT = "https://oauth.bb.com.br/oauth/token"
    USE_CERT = "server_certs/oauth.bb.com.br.cer"

    def __init__(self, client_id, client_secret, developer_key, certificate):
        self.credentials = (client_id, client_secret)
        self.certificate = certificate
        self.developer_key = developer_key
        self._token = None
        self.expires_in = None

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
        #print(self.OAUTH_ENDPOINT)
        #print(data)
        #print(self.credentials)
        resp = requests.post(self.OAUTH_ENDPOINT, data=data, verify=self.USE_CERT, auth=self.credentials)
        if resp.status_code == 401:
            raise BadCredentials()

        if resp.status_code == 400:
            raise RuntimeError(resp.json())

        json = resp.json()
        #print(f"JSON: {json}")
        self.token = json['token_type'], json['access_token']

        self.expires_in = datetime.now() + timedelta(seconds=json['expires_in'])

    def __call__(self, r):
        r.headers['Authorization'] = self.token
        r.headers['x-developer-application-key'] = self.developer_key
        r.register_hook("response", self.handle_401)
        return r


class BBAuthSandbox(BBAuth):
    OAUTH_ENDPOINT = "https://oauth.sandbox.bb.com.br/oauth/token"
    USE_CERT = "server_certs/oauth.sandbox.bb.com.br.cer"


class BBSession(requests.Session):
    ENDPOINT = "https://api-pix.bb.com.br/pix/v2/"
    USE_CERT = "server_certs/api-pix.bb.com.br.cer"

    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def request(self, method: str, path='', *args, **kwargs):
        url = self.ENDPOINT + path
        # print(url)
        resp = super().request(method, url, *args, cert=self.auth.certificate, verify=self.USE_CERT, **kwargs)
        return resp


class BBSessionSandbox(BBSession):
    ENDPOINT = "https://api-pix.hm.bb.com.br/pix/v2/"
    USE_CERT = "server_certs/api-pix.hm.bb.com.br.cer"


class BBClient:
    AUTH = BBAuth
    SESSION = BBSession

    def __init__(self, session):
        self.session = session

    @classmethod
    def from_credentials(cls, client_id: str, client_secret: str, developer_key: str, certificate: str):
        auth = cls.AUTH(client_id, client_secret, developer_key, certificate)
        session = cls.SESSION(auth)
        return cls(session)

    def request(self, method, path='', params=None, data=None, *args, **kwargs):
        resp = self.session.request(method, path=path, params=params, data=data, *args, **kwargs)
        resp.raise_for_status()
        return resp

    def received_pixs(self, init_datetime, end_datetime):
        params = {
            'inicio': init_datetime,
            'fim': end_datetime
        }

        resp = self.request('get', path='/pix', params=params)

        return resp


class BBClientSandbox(BBClient):
    AUTH = BBAuthSandbox
    SESSION = BBSessionSandbox


if __name__ == '__main__':

    client = BBClient.from_credentials(
        **env.credenciais['prod_srgold']
    )

    resp = client.received_pixs('2023-09-01T00:00:01Z', "2023-09-05T23:59:59Z")

    print(resp.json())

# {"statusCode":401,"error":"Unauthorized","message":"Bad Credentials","attributes":{"error":"Bad Credentials"}}

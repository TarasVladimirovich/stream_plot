import requests

from lib.MXserver import MXserver


class AuthManager:

    def __init__(self, mxserver: MXserver, user: str, password: str):
        self.mxserver = mxserver
        self.url = f'https://{self.mxserver.ip}:8083/SecureSphere/api/v1/auth/session'
        self.user = user
        self.password = password

    def get_auth(self):
        response = requests.post(self.url, auth=(self.mxserver.user, self.mxserver.password), verify=False)
        return response

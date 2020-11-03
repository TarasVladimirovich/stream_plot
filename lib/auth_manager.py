import requests

from lib.MXserver import MXserver


class AuthManager:

    def __init__(self, mxserver: MXserver, user: str, password: str):
        self.mxserver = mxserver
        self.user = user
        self.password = password
        self.url = f'https://{self.mxserver.ip}:8083/SecureSphere/api/v1/auth/session'

    def get_response(self):
        return requests.post(self.url, auth=(self.user, self.password), verify=False)

    def get_JSESSIONID(self):
        response = self.get_response().text
        return response[response.index(':"'):response.index(';')]

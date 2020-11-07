import requests

from lib.mxserver import MXserver


class AuthManager:

    def __init__(self, mxserver: MXserver):
        self.mxserver = mxserver
        self.url = f'https://{self.mxserver.ip}:8083/SecureSphere/api/v1/auth/session'

    def get_response(self, user=None, password=None):
        if (user or password) is None:
            user = self.mxserver.user
            password = self.mxserver.password

        return requests.post(self.url, auth=(user, password), verify=False)

    def get_JSESSIONID(self):
        response = self.get_response().text
        return response[response.index(':"')+2:response.index(';')]




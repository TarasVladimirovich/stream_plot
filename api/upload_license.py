import requests
import json

from lib.mxserver import MXserver


class UploadLicense:

    def __init__(self, mxserver: MXserver):
        self.mxserver = mxserver
        self.url = f'https://{self.mxserver.ip}:8083/SecureSphere/api/v1/administration/flex_protect'

    def register_mx(self, flex_protect, cookie_auth):
        payload = json.dumps({"licenseContent": flex_protect})
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie_auth
        }
        return requests.post(self.url, headers=headers, data=payload, verify=False)





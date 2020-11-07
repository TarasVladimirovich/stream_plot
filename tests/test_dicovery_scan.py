import logging

import requests

logger = logging.getLogger(__name__)


def test_get_scans(app):
    resp = requests.get('https://10.100.163.48:8083/SecureSphere/api/v1/conf/discovery/scans/',
                        headers={
                            'Cookie': app},
                        verify=False)
    print(resp.text)

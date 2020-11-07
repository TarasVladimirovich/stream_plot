import logging
import yaml
from pathlib import Path
from os.path import dirname, join

import pytest

from lib.mxserver import MXserver
from api.auth_manager import AuthManager

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mxserver(request):
    with open(join(dirname(Path(__file__)), 'configs/config.yaml')) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)

    mxserver = MXserver(
        ip=configs['mxIp'],
        user=configs['mxuser'],
        password=configs['password'],
        ssh_user=configs['ssh_user'],
        ssh_password=configs['ssh_password'],
    )

    def client_teardown():
        # builder = Builder([device.client.saved_filepath], [device.artifacts])
        # builder.create_file()
        log.info("\ndisconnect")
        mxserver.client.connection.disconnect()

    request.addfinalizer(client_teardown)

    return mxserver


@pytest.fixture(scope="session")
def app(request, mxserver):
    auth = AuthManager(mxserver)
    return auth.get_JSESSIONID()

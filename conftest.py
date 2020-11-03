import logging
import yaml
from pathlib import Path
from os.path import dirname, join

import pytest

from lib.MXserver import MXserver

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
        print("\ndisconnect")
        mxserver.client.connection.disconnect()

    request.addfinalizer(client_teardown)
    return mxserver


@pytest.fixture(scope="function", params=[
    (('admin', 'Barbapapa12#'), 200),
    (('admin', 'Barbapapa12'), 401),
    (('admin', ''), 401),
    (('', ''), 401),
    (('', 'Barbapapa12#'), 401),
    (('Barbapapa12#', 'Barbapapa12#'), 401),
    (('admin', 'admin'), 401),
],
                ids=['correct', 'inc pas', 'empty pass', 'empty', 'empty user', 'two pass', 'two user']
                )
def param_test_auth(request):
    return request.param


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        print(fixture)

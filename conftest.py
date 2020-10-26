import pytest
import logging

from tools.client import RemoteClient
from tools.MXserver import MXserver
from tools.builder import Builder

log = logging.getLogger(__name__)

HOST = '10.100.163.145'


@pytest.fixture(scope="session")
def mxserver(request):
    client = RemoteClient(HOST, 'root', 'Barbapapa12#')
    device = MXserver(client)

    def client_teardown():
        # builder = Builder([device.client.saved_filepath], [device.artifacts])
        # builder.create_file()
        print("\ndisconnect")
        device.client.connection.disconnect()

    request.addfinalizer(client_teardown)
    return device


@pytest.fixture(scope="function")
def profile_fixture(request):
    return request.param


@pytest.fixture(scope="function")
def resources_prepare(request, mxserver):
    log.info("==== Prepare test ====")

    def clean_setup():
        log.info("==== Clean DUT ====")

    request.addfinalizer(clean_setup)


def pytest_addoption(parser):
    parser.addoption(
        '--profile',
        action='store',
        default=3,
        type=int,
        help='Choose profile')

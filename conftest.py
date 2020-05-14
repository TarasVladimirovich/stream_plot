import pytest
import logging

from tools.connection import RemoteClient
from tools.device import Device
from tools.builder import Builder


log = logging.getLogger(__name__)


HOST = "192.168.88.236"

COMMANDS_PREPARE = ['mount -o remount,rw /', 'mkdir /usr/share/terminfo/d',
                    'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb',
                    '/ring/bin/rp set test.profile_id 6', '/ring/bin/rp set test.bitrate 2500000',
                    'systemctl restart stream']

COMMANDS_CLEAN = ['rm -rf /usr/share/terminfo/d',
                  '/ring/bin/rp unset test.profile_id', '/ring/bin/rp unset test.bitrate 2500000',
                  'systemctl restart stream', 'mount -o remount,ro /']


@pytest.fixture(scope="session")
def device(request):
    client = RemoteClient(HOST)
    device = Device(client)

    def client_teardown():
        builder = Builder([device.client.saved_filepath], [device.artifacts])
        builder.create_file()
        print("\ndisconnect")
        device.client.connection.disconnect()

    request.addfinalizer(client_teardown)
    return device


@pytest.fixture(scope="function", params=[
    (0, '(640x360)'),
    (1, '(848x480)'),
    (2, '(1280x720)'),
    (3, '(1920x1080)'),
])
def profile_fixture(request):
    return request.param


@pytest.fixture(scope="function")
def resources_prepare(request, device):
    log.info("==== Prepare test ====")
    log.info('Prepare setup \n {}'.format(' ;\n '.join(COMMANDS_PREPARE)))
    device.client.execute_commands(COMMANDS_PREPARE)

    def clean_setup():
        log.info("==== Clean DUT ====")
        log.info('Clean setup \n {}'.format(' ;\n '.join(COMMANDS_CLEAN)))
        device.client.execute_commands(COMMANDS_CLEAN)

    request.addfinalizer(clean_setup)

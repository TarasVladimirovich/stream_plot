import pytest
import logging

from tools.connection import RemoteClient


log = logging.getLogger(__name__)


HOST = "192.168.88.236"

COMMANDS_PREPARE = ['mount -o remount,rw /', 'mkdir /usr/share/terminfo/d',
                    'cp /usr/share/terminfo/v/vt100 /usr/share/terminfo/d/dumb',
                    '/ring/bin/rp set test.profile_id 3', '/ring/bin/rp set test.bitrate 2500000',
                    'systemctl restart stream']

COMMANDS_CLEAN = ['rm -rf /usr/share/terminfo/d',
                  '/ring/bin/rp unset test.profile_id 3', '/ring/bin/rp unset test.bitrate 2500000',
                  'systemctl restart stream', 'mount -o remount,ro /']


@pytest.fixture(scope="session")
def client_setup(request):
    client = RemoteClient(HOST)

    def client_teardown():
        print("\ndisconnect")
        client.connection.disconnect()

    request.addfinalizer(client_teardown)

    return client


@pytest.fixture(scope="function")
def resources_prepare(request, client_setup):
    log.info("==== Prepare test ====")
    log.info('Prepare setup \n {}'.format(' ;\n '.join(COMMANDS_PREPARE)))
    client_setup.execute_commands(COMMANDS_PREPARE)

    def clean_setup():
        log.info("==== Clean DUT ====")
        log.info('Clean setup \n {}'.format(' ;\n '.join(COMMANDS_CLEAN)))
        client_setup.execute_commands(COMMANDS_CLEAN)

    request.addfinalizer(clean_setup)

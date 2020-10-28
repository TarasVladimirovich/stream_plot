import logging
import pytest
from pathlib import Path
import yaml

from lib.MXserver import MXserver

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mxserver(request):

    abs_path = Path(__file__).parent
    with open(f'{abs_path}\\configs\\config.yaml') as file:
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


@pytest.fixture(scope="function")
def resources_prepare(request, mxserver):
    log.info("==== Prepare test ====")

    def clean_setup():
        log.info("==== Clean DUT ====")

    request.addfinalizer(clean_setup)


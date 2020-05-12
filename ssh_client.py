from sys import argv
import logging

from tools.connection import RemoteClient
from tests.test_resources_consumption import test_5_min

from tools.builder import Builder
from tools.device import Device

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)-100s %(filename)s:%(funcName)s:%(lineno)d',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.INFO,
                    )

log = logging.getLogger(__name__)


if __name__ == '__main__':
    client = RemoteClient(argv[1].strip())
    device = Device(client)

    # test_5_min(device)

    log.info("Create file")
    builder = Builder([device.client.saved_filepath])
    builder.create_file()
    log.info("File crated")
    device.client.connection.disconnect()
    log.info('====Done====')



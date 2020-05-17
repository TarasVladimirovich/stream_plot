from sys import argv
import logging
import sys

from tools.client import RemoteClient
from tools.resources import test_5_min


from tools.builder import Builder
from tools.device import Device
from tools.client import RemoteClient

logging.basicConfig(format='%(asctime)s %(filename)25s:%(lineno)-4d %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler(sys.stdout)]
                    )

log = logging.getLogger(__name__)


if __name__ == '__main__':
    client = RemoteClient('192.168.88.236')
    device = Device(client)
    test_5_min(device)

    log.info("Create file")
    builder = Builder([device.client.saved_filepath], device.artifacts, device.avg_resources())
    builder.create_file()
    log.info("File crated")
    device.client.connection.disconnect()
    log.info('====Done====')



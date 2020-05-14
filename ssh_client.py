from sys import argv
import logging

from tools.client import RemoteClient
from tools.resources import test_5_min


from tools.builder import Builder
from tools.device import Device
from tools.client import RemoteClient

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)-100s %(filename)s:%(funcName)s:%(lineno)d',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.INFO,
                    )

log = logging.getLogger(__name__)


if __name__ == '__main__':
    client = RemoteClient('192.168.88.236')
    device = Device(client)

    # test_5_min(device)

    log.info("Create file")
    builder = Builder(['/Users/taraskoshletskyi/PycharmProjects/stream_plot/files/Stream-SIP-99.0.5649d-ORION_V1B1S10.txt'],
                      device.artifacts, device.resources)
    builder.create_file()
    log.info("File crated")
    device.client.connection.disconnect()
    log.info('====Done====')



import logging
import sys

from tools.builder import Builder
from tools.device import Device
from tools.resources import test_5_min
from tools.client import RemoteClient

import click

logging.basicConfig(format='%(asctime)s %(filename)25s:%(lineno)-4d %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler(sys.stdout)]
                    )

log = logging.getLogger(__name__)


@click.command()
@click.option('--ip-addr', default='', help='Insert ip addres.', type=str)
@click.option('--profile',  default=6, help='Choose profile.', type=int)
@click.option('--bitrate',  default=2500000, help='Set bitrate.', type=int)
def main(ip_addr, profile, bitrate):
    client = RemoteClient(ip_addr)
    device = Device(client)
    test_5_min(device, profile, bitrate)

    log.info("Create file")
    builder = Builder([device.client.saved_filepath], device.artifacts, device.avg_resources())
    builder.create_file()
    device.client.connection.disconnect()
    log.info('====Done====')


if __name__ == '__main__':
    main()



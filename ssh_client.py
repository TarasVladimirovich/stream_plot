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
# @click.option('--profile',  default=None, help='Choose profile.', type=int)
# @click.option('--bitrate',  default=None, help='Set bitrate.', type=int)
# @click.option('--idle', is_flag=True, help='set flag, if need check IDLE')
def main(ip_addr, profile, bitrate, idle):
    client = RemoteClient(ip_addr)
    device = Device(client)
    test_5_min(device, profile, bitrate, idle)

    log.info("Create file")
    builder = Builder([device.client.saved_filepath], device.artifacts, device.avg_resources(idle))
    builder.create_file()
    device.client.connection.disconnect()
    log.info('====Done====')


if __name__ == '__main__':
    main()



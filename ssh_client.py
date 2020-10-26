import logging
import sys

from tools.MXserver import MXserver
from lib.resources_monitor import test_5_min
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
@click.option('--user', default='root', help='Input server user.', type=str)
@click.option('--password', default='Barbapapa12#', help='Input server password.', type=str)
def main(ip_addr, user, password):
    client = RemoteClient(ip_addr, user, password)
    mxserver = MXserver(client)
    # mxserver.client.execute_command('ping 8.8.8.8')
    test_5_min(mxserver)
    # log.info("Create file")
    # builder = Builder([device.client.saved_filepath], device.artifacts, device.avg_resources(idle))
    # builder.create_file()
    mxserver.client.connection.disconnect()
    log.info('====Done====')


if __name__ == '__main__':
    main()

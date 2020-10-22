import logging
import sys

from tools.builder import Builder
from tools.MXserver import MXserver
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
@click.option('--user', default='root', help='Input server user.', type=str)
@click.option('--password', default='Barbapapa12#', help='Input server password.', type=str)
def main(ip_addr, user, password):
    client = RemoteClient(ip_addr, user, password)
    mxserver = MXserver(client)
    mxserver.client.execute_command(" timeout 60 top -b -d 1 -p 32018 | awk '/^%Cpu0/{id0=$9; sy0=$5} "
                                    "/^%Cpu1/{id1=$9; sy1=$5} /^%Cpu2/{id2=$9; sy2=$5} "
                                    "/^%Cpu3/{id3=$9; sy3=$5} "
                                    "/32018+ mxserver/{print id0,sy0,id1,sy1,id2,sy2,id3,sy3,mem,$9,$10}'"
                                    " >> /tmp/tarastest.txt&")
    # test_5_min(mxserver)
    #
    # log.info("Create file")
    # builder = Builder([device.client.saved_filepath], device.artifacts, device.avg_resources(idle))
    # builder.create_file()
    # device.client.connection.disconnect()
    log.info('====Done====')


if __name__ == '__main__':
    main()

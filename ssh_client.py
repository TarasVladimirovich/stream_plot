from sys import argv
import logging

from tools.client import RemoteClient
from tests.resources_consumption import test_5_min

from tools.builder import Builder

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)-100s %(filename)s:%(funcName)s:%(lineno)d',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.INFO,
                    )

log = logging.getLogger(__name__)


if __name__ == '__main__':
    client = RemoteClient(argv[1].strip())
    log.info(f"Create file{client.file_name}")

    test_5_min(client=client, file_name=client.file_name)

    builder = Builder([client.saved_filepath])
    builder.create_file()

    client.disconnect()
    log.info('====Done====')



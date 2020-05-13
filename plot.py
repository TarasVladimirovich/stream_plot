from sys import argv

from tools.builder import Builder
from tools.device import Device
from tools.connection import RemoteClient


if __name__ == '__main__':
    builder = Builder(argv[1:])
    builder.create_file()
    print('Done')


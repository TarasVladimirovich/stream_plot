import logging

logger = logging.getLogger(__name__)


class COMMAND:
    SERVER = 'server'
    VERSION = '--version'
    VERBOSE = '--verbose'


class ServerOption:
    STATUS = 'status'
    START = 'start'
    STOP = 'stop'


class IMPCTL:

    BINARY_PATH = '/opt/SecureSphere/etc/impctl/bin/impctl'

    def __init__(self, client):
        self.client = client

    def _run_command(self, *args):
        command = f'{self.BINARY_PATH}'
        for c in args:
            command += f' {c}'
        return self.client.execute_command(command)

    def server(self, option_: ServerOption):
        """ Control server"""
        return self._run_command(COMMAND.SERVER, option_)

    def check_version_verbose(self):
        return self._run_command(COMMAND.VERSION, COMMAND.VERBOSE)

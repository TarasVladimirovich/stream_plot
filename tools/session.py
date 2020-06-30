import logging
from os import path, system

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from scp import SCPClient


log = logging.getLogger(__name__)


class ClientHelper:

    def __init__(self, connection):
        self.connection = connection

    def __check_ping(self):
        log.info(f'ping {self.connection.host}')
        response = system(f'ping -c 1 {self.connection.host} >/dev/null 2>&1 ')
        if response == 0:
            log.info("Host is active, proceed the test")
        else:
            log.error('host is unreachable')
            exit(1)
        return response

    def connect(self):
        """
        Open connection to remote host.
        :return: client
        """

        self.__check_ping()
        try:
            client = SSHClient()
            client.load_host_keys(path.expanduser('~/.ssh/known_hosts'))
            client.set_missing_host_key_policy(AutoAddPolicy)
            client.connect(self.connection.host,
                           username=self.connection.user,
                           password='',
                           look_for_keys=False,
                           timeout=5000)
        except AuthenticationException as error:
            log.error(f'{error}, exit program')
            exit(1)
        else:
            log.info('Create client')
            return client

    def create_scp_session(self):
        """
        Open connection to remote host.
        :return: scp
        """
        try:
            scp = SCPClient(self.connection.client.get_transport())
        except AuthenticationException as error:
            log.error(f'{error}, exit program')
            exit(1)
        else:
            log.info('Create scp transport')
            return scp

    def disconnect(self):
        """Close ssh connection."""
        self.connection.client.close()
        self.connection.scp.close()
        log.info('Disconnected')

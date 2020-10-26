import logging
from os import devnull
from subprocess import check_call, CalledProcessError

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from scp import SCPClient

log = logging.getLogger(__name__)


class ClientHelper:

    def __init__(self, connection):
        self.connection = connection

    def __check_ping(self):
        with open(devnull, 'w') as DEVNULL:
            try:
                check_call(
                    ['ping', '-n', '1', self.connection.host],
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
                is_up = 0
            except CalledProcessError:
                is_up = 1
        log.info(f'ping {self.connection.host}')
        if is_up == 0:
            log.info("Host is active, proceed the test")
        else:
            log.error('host is unreachable')
            exit(1)
        return is_up

    def connect(self):
        """
        Open connection to remote host.
        :return: client
        """

        self.__check_ping()
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy)
            client.connect(self.connection.host,
                           username=self.connection.user,
                           password=self.connection.password,
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


if __name__ == '__main__':
    def __check_ping(host):
        import os
        import subprocess

        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', '-n', '1', host],
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
                is_up = 0
            except subprocess.CalledProcessError:
                is_up = 1
        return is_up


    print(__check_ping('10.100.163.145'))

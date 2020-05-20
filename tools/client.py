from os import path, makedirs
from pathlib import Path
import sys

import logging
from scp import SCPException

from tools.session import ClientHelper

log = logging.getLogger(__name__)


class RemoteClient:

    def __init__(self, host, user='root', ssh_key_filepath='', remote_path=''):
        self.host = host
        self.user = user
        self.connection = ClientHelper(self)
        self.client = self.connection.connect()
        self.scp = self.connection.create_scp_session()
        self.saved_filepath = ''
        # self.ssh_key_filepath = ssh_key_filepath
        # self.remote_path = remote_path

    def download_file(self, file):
        """
        Download file from remote host.

        :param file: File name from remote host.
        :return: String with file path
        """
        abs_path = Path(__file__).parent.parent
        makedirs(f'{abs_path}/files', exist_ok=True)
        try:
            self.scp.get(f'{file}', path.join(abs_path, 'files'))
            self.saved_filepath = f"{abs_path}/files/{file.replace('/tmp/', '')}"
            log.info(f'{file} file copied to {self.saved_filepath}')
        except SCPException as error:
            log.error(error)
            raise SCPException

    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        """
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            status = stdout.channel.recv_exit_status()
            if status == 0:
                response = stdout.readlines()
                for line in response:
                    log.info(f'stdout: {line}')
            else:
                for line in stderr.readlines():
                    log.error(f'stderr: {line}')

    def execute_command(self, cmd):
        """
        Execute command in succession.

        :param cmd: Unix command as strings.
        :return: String with information
        """
        info = ''
        stdin, stdout, stderr = self.client.exec_command(cmd)
        status = stdout.channel.recv_exit_status()
        if status == 0:
            info = stdout.read().decode().strip()
            log.debug(f'Return next information {info}')
        else:
            for line in stderr.readlines():
                log.error('stderr: ', line)
        return info

    # for future upload files to remote host
    # def bulk_upload(self, files):
    #     """
    #     Upload multiple files to a remote directory.
    #
    #     :param files: List of strings representing file paths to local files.
    #     """
    #     if self.client_setup is None:
    #         self.client_setup = self.__connect()
    #     uploads = [self.__upload_single_file(file) for file in files]
    #
    # def __upload_single_file(self, file):
    #     """Upload a single file to a remote directory."""
    #     try:
    #         self.scp.put(file,
    #                      recursive=True,
    #                      remote_path=self.remote_path)
    #     except SCPException as error:
    #         print(error)
    #         raise error
    #     finally:
    #         pass


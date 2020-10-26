from os import path, makedirs
from pathlib import Path

import logging
from scp import SCPException

from tools.session import ClientHelper

log = logging.getLogger(__name__)


class RemoteClient:

    def __init__(self, host, user, password, ssh_key_filepath='', remote_path=''):
        self.host = host
        self.user = user
        self.password = password
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

    def execute_commands(self, commands: list):
        for cmd in commands:
            self.execute_command(cmd)

    def execute_command(self, cmd: str):
        """
        Execute command in succession.

        :param cmd: Unix command as strings.
        :return: String with information
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        status = stdout.channel.recv_exit_status()
        log.info(f'Execute command: {cmd}')
        if status == 0:
            response = stdout.readlines()
            if len(response) == 1:
                response = response[0].strip()
                log.info(response)
                return response
            else:
                for line in response:
                    log.info(line)
        else:
            for line in stderr.readlines():
                log.error(line)

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

from os import path, makedirs, getcwd, system
import datetime
import logging

import yaml

from tools.client import ClientHelper

log = logging.getLogger(__name__)


class RemoteClient:

    def __init__(self, host, user='root', ssh_key_filepath='', remote_path=''):
        self.host = host
        self.user = user
        self.connection = ClientHelper(self)
        self.client = self.connection.connect()
        self.scp = self.connection.create_scp_session()
        self.artifacts = self.get_artifacts()
        self.saved_filepath = ''
        # self.ssh_key_filepath = ssh_key_filepath
        # self.remote_path = remote_path

    @property
    def file_name(self):
        return f'Stream-{self.artifacts["solution"]}-{self.artifacts["fw"]}-{self.artifacts["board_version"]}.txt'

    def download_file(self, file):
        """
        Download file from remote host.

        :param file: File name from remote host.
        :return: String with file path
        """
        try:
            makedirs('files', exist_ok=True)
        except OSError as error:
            self.scp.get(f'{file}')
            self.saved_filepath = f'{self.file_name}'
            log.error(error)
            log.error(f'{file} file copied to {getcwd()}')
        else:
            self.scp.get(f'{file}', path.join('files'))
            self.saved_filepath = f'files/{self.file_name}'
            log.info(f'{file} file copied to files folder')

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
                    log.info(f'stderr: {line}')
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
            log.info(f'Return next information {info}')
        else:
            for line in stderr.readlines():
                log.error('stderr: ', line)
        return info

    def get_artifacts(self):
        """Collect artifacts from DUT"""
        artifacts = dict()
        with open('configs/artifacts.yaml') as file:
            tmp = yaml.load(file, Loader=yaml.FullLoader)
        for k, v in tmp.items():
            artifacts[k] = self.execute_command(v)
        if 'unset' in artifacts['solution']:
            artifacts['solution'] = 'SIP'
        else:
            artifacts['solution'] = 'RMS'
        artifacts['date'] = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        return artifacts

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


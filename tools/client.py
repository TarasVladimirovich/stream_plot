from os import path, makedirs, getcwd, system
import datetime
import logging

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from scp import SCPClient
import yaml

log = logging.getLogger(__name__)


class RemoteClient:

    def __init__(self, host, user='root', ssh_key_filepath='', remote_path=''):
        self.host = host
        self.user = user
        self.client = None
        self.scp = None
        self.artifacts = self.get_artifacts()
        self.file_name = f'Stream-{self.artifacts["solution"]}-{self.artifacts["fw"]}-{self.artifacts["board_version"]}.txt'
        self.saved_filepath = ''
        # self.ssh_key_filepath = ssh_key_filepath
        # self.remote_path = remote_path

    def __check_ping(self):
        log.info(f'ping {self.host}')
        response = system(f'ping -c 1 {self.host} >/dev/null 2>&1 ')
        if response == 0:
            log.info("Host is active, proceed the test")
        else:
            log.error('host is unreachable')
            exit(1)
        return response

    def __connect(self):
        """Open connection to remote host."""
        self.__check_ping()
        try:
            self.client = SSHClient()
            self.client.load_host_keys(path.expanduser('~/.ssh/known_hosts'))
            self.client.set_missing_host_key_policy(AutoAddPolicy)
            self.client.connect(self.host,
                                username=self.user,
                                password='',
                                look_for_keys=False,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as error:
            log.error(f'{error}, exit program')
            exit(1)
        else:
            log.info('Create client')
            return self.client

    def disconnect(self):
        """Close ssh connection."""
        self.client.close()
        self.scp.close()
        log.info('Disconnected')

    # for future upload files to remote host
    # def bulk_upload(self, files):
    #     """
    #     Upload multiple files to a remote directory.
    #
    #     :param files: List of strings representing file paths to local files.
    #     """
    #     if self.client is None:
    #         self.client = self.__connect()
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

    def download_file(self, file):
        """
        Download file from remote host.

        :param file: File name from remote host.
        :return: String with file path
        """
        if self.scp is None:
            self.scp = self.__connect()
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
        if self.client is None:
            log.error('Create client')
            self.client = self.__connect()
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
        if self.client is None:
            self.client = self.__connect()
        info = ''
        stdin, stdout, stderr = self.client.exec_command(cmd)
        status = stdout.channel.recv_exit_status()
        if status == 0:
            info = stdout.read().decode().strip()
            log.info(f'Collected next artifacts {info}')
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


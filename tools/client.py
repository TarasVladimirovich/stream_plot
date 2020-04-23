from os import path, makedirs, getcwd
import datetime

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException
from scp import SCPClient
import yaml


class RemoteClient:

    def __init__(self, host, user='root', ssh_key_filepath='', remote_path=''):
        self.host = host
        self.user = user
        self.client = self.__connect()
        # self.ssh_key_filepath = ssh_key_filepath
        # self.remote_path = remote_path

    def __connect(self):
        """Open connection to remote host."""
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
            print(error)
            raise error
        finally:
            return self.client

    def disconnect(self):
        """Close ssh connection."""
        self.client.close()
        self.scp.close()

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
        """Download file from remote host."""
        if self.client is None:
            self.client = self.__connect()
        try:
            makedirs('files', exist_ok=True)
        except OSError as error:
            print(error)
            self.scp.get(f'/tmp/{file}', getcwd())
        else:
            self.scp.get(f'/tmp/{file}', path.join('files'))

    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        """
        if self.client is None:
            self.client = self.__connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            status = stdout.channel.recv_exit_status()
            if status == 0:
                response = stdout.readlines()
                for line in response:
                    print(line, end='')
            else:
                for line in stderr.readlines():
                    print('stderr: ', line, end='')

    def get_info_from_remote_host(self, cmd):
        """
        Execute command in succession.

        :param command: Unix command as strings.
        :return: String with information
        """
        if self.client is None:
            self.client = self.__connect()
        info = None
        stdin, stdout, stderr = self.client.exec_command(cmd)
        status = stdout.channel.recv_exit_status()
        if status == 0:
            info = stdout.read().decode().strip()
        else:
            print(f'{cmd} hasn"t received')
        return info

    def get_artifacts(self):
        """Collect artifacts from DUT"""
        artifacts = dict()
        with open ('configs/artifacts.yaml') as file:
            tmp = yaml.load(file, Loader=yaml.FullLoader)
        for k, v in tmp.items():
            artifacts[k] = self.get_info_from_remote_host(v)
        if 'unset' in artifacts['solution']:
            artifacts['solution'] = 'SIP'
        else:
            artifacts['solution'] = 'RMS'
        artifacts['date'] = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        return artifacts


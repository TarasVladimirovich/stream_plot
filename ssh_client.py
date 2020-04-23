from sys import argv

from tools.client import RemoteClient
from tests.resources_consumption import test_5_min

from tools.builder import Builder

HOST = '192.168.88.237'


# def check_ping():
#     response = os.system('ping -c 1 ' + HOST)
#     if response == 0:
#         ping_status = 'Network Active'
#     else:
#         ping_status = 'Network Error'
#     return ping_status


# def connect():
#
#     client = SSHClient()
#     client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
#     client.set_missing_host_key_policy(AutoAddPolicy)
#
#     client.connect(HOST, username=USERNAME, password=PASSWORD, look_for_keys=False)
#
#     return client


if __name__ == '__main__':
    client = RemoteClient(argv[1])
    artifacts = client.get_artifacts()
    file_name = f'Stream-{artifacts["solution"]}-{artifacts["fw"]}-{artifacts["board_version"]}'
    artifacts.update(test_5_min(client=client, file_name=file_name))
    client.download_file(file=file_name)
    builder = Builder([f'files/{file_name}'])
    builder.create_file()
    print('Done')



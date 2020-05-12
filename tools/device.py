import datetime
from tools.connection import RemoteClient
from time import sleep
from pathlib import Path

import yaml


class Device:

    PROFILES = {
                 0: 234567,
                 1: 534567,
                 2: 1234567,
                 3: 1534567,
                }

    def __init__(self, client):
        self.client = client
        self.artifacts = self.get_artifacts()

    @property
    def file_name(self):
        return f'Stream-{self.artifacts["solution"]}-{self.artifacts["fw"]}-{self.artifacts["board_version"]}.txt'

    def set_profile(self, profile=0):
        if profile > 3:
            profile = 3
        elif profile < 0:
            profile = 0
        self.client.execute_commands([f'/ring/bin/rp set stream.probed_bitrate {self.PROFILES[profile]}',
                                      'systemctl restart stream'])
        sleep(5)

    def show_stream_info(self):
        info = self.client.execute_command('test_encode --show-stream-info | grep Resolution')
        return info.split('\n')[0].split(':')[1].strip()

    def get_artifacts(self):
        """Collect artifacts from DUT"""
        artifacts = dict()
        abs_path = Path(__file__).parent.parent
        with open(f'{abs_path}/configs/artifacts.yaml') as file:
            tmp = yaml.load(file, Loader=yaml.FullLoader)
        for k, v in tmp.items():
            artifacts[k] = self.client.execute_command(v)
        if 'unset' in artifacts['solution']:
            artifacts['solution'] = 'SIP'
        else:
            artifacts['solution'] = 'RMS'
        artifacts['date'] = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        return artifacts


if __name__ == '__main__':

    d = Device(RemoteClient('192.168.88.236'))
    print(d.get_artifacts())

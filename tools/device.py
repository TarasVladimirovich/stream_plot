import datetime
from tools.client import RemoteClient
from time import sleep
from pathlib import Path
import numpy as np

import yaml

from tools.reader import Reader


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
        # self.resources = self.avg_resources()
        self.resources = {'average': {'idle': 22.707, 'stream': 15.446, 'memory': 9.766, 'sys': 22.702},
                          'ding_1': {'idle': 42.75, 'stream': 3.665, 'memory': 8.871, 'sys': 18.629},
                          'ding_2': {'idle': 26.619, 'stream': 14.914, 'memory': 9.597, 'sys': 29.69}}

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

    def avg_resources(self):
        """
        HardCode Function
        :return:
        """
        df = Reader(self.client.saved_filepath).reader()
        temp = {'average': dict(),
                'ding_1': dict(),
                'ding_2': dict(),
                }
        for data in df:
            if df[data].dtypes != np.float64:
                for i in range(df[data].size):
                    try:
                        float(df[data][i])
                    except ValueError:
                        df.iloc[i, df.columns.get_loc(data)] = df[data][i - 1]
                df[data] = df.astype('float64')
            temp['average'].update({data: round(sum(df[data]) / df[data].size, 3)})
            temp['ding_1'].update({data: round(sum(df[data].loc[30:91]) / df[data].loc[30:91].size, 3)})
            temp['ding_2'].update({data: round(sum(df[data].loc[120:271]) / df[data].loc[120:271].size, 3)})
        return temp


if __name__ == '__main__':


    d = Device(RemoteClient('192.168.88.236'))
    print('qq')



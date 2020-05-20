import datetime
from time import sleep
from pathlib import Path
import numpy as np
from math import isnan

import yaml

from tools.iohelper import IOhelper


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

    def avg_resources(self):
        """
        HardCode Function
        :return: Dictionary with resources
        """
        df = IOhelper().reader(self.client.saved_filepath)
        temp = {'average': dict(),
                'ding_1': dict(),
                'ding_2': dict(),
                }
        for data in df:
            tmp_number = 0
            for i in range(df[data].size):
                try:
                    float(df[data][i])
                    if isnan(float(df[data][i])):
                        df.iloc[i, df.columns.get_loc(data)] = tmp_number
                    tmp_number = float(df[data][i])
                except ValueError:
                    df.iloc[i, df.columns.get_loc(data)] = tmp_number
            if df[data].dtypes != np.float64:
                df[data] = df[data].astype(float)

            temp['average'].update({data: round(sum(df[data]) / df[data].size, 3)})
            temp['ding_1'].update({data: round(sum(df[data].loc[5*30:5*91]) / df[data].loc[5*30:5*91].size, 3)})
            temp['ding_2'].update({data: round(sum(df[data].loc[5*120:5*271]) / df[data].loc[5*120:5*271].size, 3)})
        return temp


if __name__ == '__main__':
    """
    """
    # from tools.client import RemoteClient
    # import time
    #
    # device = Device(RemoteClient('192.168.88.236'))
    #
    # pid_stream = device.client.execute_command("systemctl status stream | awk '/Main PID/{print $3}'")
    # pid_pulse = device.client.execute_command("systemctl status pulseaudio | awk '/Main PID/{print $3}'")
    # pid_ivaapp = device.client.execute_command("systemctl status ivaapp | awk '/Main PID/{print $3}'")
    # time.sleep(3)
    #
    # command = f"top -b -d 0.2 -p {pid_stream}, {pid_pulse}, {pid_ivaapp} " \
    #           f"| awk '/^%Cpu/{{idle=$8, sys=$4}} /{pid_stream}+ root/{{cpu=$9, mem=$10}} " \
    #           f"/{pid_ivaapp}+ root/{{cpuiv=$9}} " \
    #           f"/{pid_pulse}+ pulse/{{print idle,cpu,mem,$9,$10,cpuiv,sys}}' >> /tmp/{device.file_name} & "
    #
    # print(command)

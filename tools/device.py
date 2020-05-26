import datetime
import logging
from pathlib import Path
import numpy as np
from math import isnan
from time import strftime

import yaml

from tools.iohelper import IOhelper
from lib.ipc import IPC
from lib.rp import RP


logger = logging.getLogger(__name__)


class Device:

    # PROFILES = {
    #              0: 234567,
    #              1: 534567,
    #              2: 1234567,
    #              3: 1534567,
    #             }

    def __init__(self, client):
        self.client = client
        self.artifacts = self.get_artifacts()
        self.timestr = strftime('%d-%m-%Y_%H:%M')
        self.ipc = IPC(self.client)
        self.rp = RP(self.client)

    @property
    def file_name(self):
        return f'{self.timestr}_Stream-{self.artifacts["solution"]}-{self.artifacts["fw"]}-' \
               f'{self.artifacts["board_version"]}.txt'

    def restart_service(self, service='stream'):
        logger.info(f'restart service {service}')
        self.client.execute_command(f'systemctl restart {service}')

    def make_write_fs(self):
        logger.info('make file system for writing')
        self.client.execute_command('mount -o remount,rw /')

    def make_read_fs(self):
        logger.info('make file reead only')
        self.client.execute_command('mount -o remount,ro /')

    def service_pid(self, service: str) -> str:
        return self.client.execute_command(
            f"systemctl status {service} | awk '/Main PID/{{print $3}}'")

    def show_stream_info(self):
        info = (
            self.client.execute_command(
                "test_encode --show-stream-info | awk 'FNR==8{res=$3} FNR==13{print res, $4}' "
            )
        )
        return info

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
    # c = RemoteClient('192.168.88.236')
    # d = Device(c)
    # pid_stream, pid_pulse, pid_ivaapp = d.service_pid('stream'), \
    #                                     d.service_pid('pulseaudio'), d.service_pid('ivaapp')
    # print(pid_stream)
    # print(pid_pulse)
    # print(pid_ivaapp)

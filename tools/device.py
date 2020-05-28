import datetime
import logging
from pathlib import Path
from time import strftime

import pandas as pd
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
        artifacts['solution'] = 'SIP' if 'unset' in artifacts['solution'] else 'RMS'
        artifacts['date'] = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        return artifacts

    def avg_resources(self):
        """
        Need to refactor
        :return: Dictionary with resources
        """
        df = IOhelper().reader(self.client.saved_filepath)
        # df = IOhelper().reader(
        #     "/Users/taraskoshletskyi/Downloads/1.txt"
        # )
        for data in df:
            df[data] = pd.to_numeric(df[data], errors='coerce')
        df = df.fillna(0)

        temp = {'average': dict(),
                'before': dict(),
                'ding_1': dict(),
                'between': dict(),
                'ding_2': dict(),
                'after': dict(),
                }

        for data in df:
            temp['average'].update(
                {data: round(df[data].sum() / df[data].size, 3)})
            temp['before'].update(
                {data: round((df[data].loc[:2*29].sum()) / df[data].loc[:2*29].size, 3)})
            temp['ding_1'].update(
                {data: round(df[data].loc[2*30:2*91].sum() / df[data].loc[2*30:2*91].size, 3)})
            temp['between'].update(
                {data: round(df[data].loc[2*92:2*119].sum() / df[data].loc[2*92:2*119].size, 3)})
            temp['ding_2'].update(
                {data: round(df[data].loc[2*120:2*271].sum() / df[data].loc[2*120:2*271].size, 3)})
            temp['after'].update(
                {data: round(df[data].loc[2*271:].sum() / df[data].loc[2*271:].size, 3)})
        return temp


if __name__ == '__main__':
    """
    """
    from tools.client import RemoteClient
    c = RemoteClient('192.168.88.236')
    d = Device(c)
    pid_stream, pid_pulse, pid_ivaapp = d.service_pid('stream'), \
        d.service_pid('pulseaudio'), d.service_pid('ivaapp')

    logger.info('==== Start test =====')

    command = f"timeout -t 3600 top -b -d 0.5 -p {pid_stream}, {pid_pulse}, {pid_ivaapp} " \
              f"| awk '/^%Cpu/{{idle=$8, sys=$4}} " \
              f"/{pid_stream}+ root/{{cpu=$9, mem=$10}} " \
              f"/{pid_ivaapp}+ root/{{cpuiv=$9}} " \
              f"/{pid_pulse}+ pulse/{{print idle,cpu,mem,$9,$10,cpuiv,sys}}' >> /root/2.3.00050d.txt & "

    print(command)

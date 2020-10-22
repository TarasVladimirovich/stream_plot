import datetime
import logging
from pathlib import Path
from time import strftime

import pandas as pd
import yaml

from tools.iohelper import IOhelper
from lib.impctl import IMPCTL

logger = logging.getLogger(__name__)


class MXserver:

    def __init__(self, client):
        self.client = client
        self.__artifacts = None
        self.__file_name = None
        self.impctl = IMPCTL(self.client)

    @property
    def file_name(self):

        # if self.__file_name is None:
        #     timestr = strftime('%d-%m-%YT%H_%M')
        #     self.__file_name = f'{timestr}_Stream-{self.artifacts["solution"]}-{self.artifacts["fw"]}-' \
        #                        f'{self.artifacts["board_version"]}.txt'

        # return self.__file_name
        return 'tarastest.txt'

    @property
    def artifacts(self):
        """
        Need to refactor
        :return: Dictionary with artifacts
        """
        if self.__artifacts is None:
            artifacts = dict()
            abs_path = Path(__file__).parent.parent
            with open(f'{abs_path}/configs/artifacts.yaml') as file:
                tmp = yaml.load(file, Loader=yaml.FullLoader)
            for k, v in tmp.items():
                artifacts[k] = self.client.execute_command(v)
            artifacts['date'] = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
            self.__artifacts = artifacts

        return self.__artifacts

    def restart_service(self, service):
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

    def pidof(self, program: str) -> str:
        return self.client.execute_command(f"pidof {program}")

    def avg_resources(self, idle=False):
        """
        Need to refactor
        :return: Dictionary with resources
        """
        df = IOhelper().reader(self.client.saved_filepath)
        for data in df:
            df[data] = pd.to_numeric(df[data], errors='coerce')
        df = df.fillna(0)

        if idle:
            temp = {'average': dict()}
            for data in df:
                temp['average'].update(
                    {data: round(df[data].sum() / df[data].size, 3)})
        else:
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
                    {data: round((df[data].loc[:2 * 29].sum()) / df[data].loc[:2 * 29].size, 3)})
                temp['ding_1'].update(
                    {data: round(df[data].loc[2 * 30:2 * 91].sum() / df[data].loc[2 * 30:2 * 91].size, 3)})
                temp['between'].update(
                    {data: round(df[data].loc[2 * 92:2 * 119].sum() / df[data].loc[2 * 92:2 * 119].size, 3)})
                temp['ding_2'].update(
                    {data: round(df[data].loc[2 * 120:2 * 271].sum() / df[data].loc[2 * 120:2 * 271].size, 3)})
                temp['after'].update(
                    {data: round(df[data].loc[2 * 271:].sum() / df[data].loc[2 * 271:].size, 3)})
        return temp

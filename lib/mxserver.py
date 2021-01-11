import datetime
import logging
from pathlib import Path
from time import strftime

import pandas as pd

from tools.iohelper import IOhelper
from lib.impctl import IMPCTL
from tools.ssh_client import SSHClient


logger = logging.getLogger(__name__)


class MXserver:

    def __init__(self, ip, user, password, ssh_user, ssh_password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.client = SSHClient(self.ip, self.ssh_user, self.ssh_password)
        self.impctl = IMPCTL(self.client)

    @property
    def file_name(self):
        return 'tarastest.txt'

    def restart_service(self, service):
        logger.info(f'restart service {service}')
        self.client.execute_command(f'systemctl restart {service}')

    def service_pid(self, service: str) -> str:
        return self.client.execute_command(
            f"systemctl status {service} | awk '/Main PID/{{print $3}}'")

    def pidof(self, program: str) -> str:
        return self.client.execute_command(f"pidof {program}")

    def __str__(self):
        return f'ip: {self.ip}, user: {self.user}, ' \
               f'password: {self.password}'

    # def avg_resources(self, idle=False):
    #     """
    #     Need to refactor
    #     :return: Dictionary with resources
    #     """
    #     df = IOhelper().reader(self.client.saved_filepath)
    #     for data in df:
    #         df[data] = pd.to_numeric(df[data], errors='coerce')
    #     df = df.fillna(0)
    #
    #     if idle:
    #         temp = {'average': dict()}
    #         for data in df:
    #             temp['average'].update(
    #                 {data: round(df[data].sum() / df[data].size, 3)})
    #     else:
    #         temp = {'average': dict(),
    #                 'before': dict(),
    #                 'ding_1': dict(),
    #                 'between': dict(),
    #                 'ding_2': dict(),
    #                 'after': dict(),
    #                 }
    #
    #         for data in df:
    #             temp['average'].update(
    #                 {data: round(df[data].sum() / df[data].size, 3)})
    #             temp['before'].update(
    #                 {data: round((df[data].loc[:2 * 29].sum()) / df[data].loc[:2 * 29].size, 3)})
    #             temp['ding_1'].update(
    #                 {data: round(df[data].loc[2 * 30:2 * 91].sum() / df[data].loc[2 * 30:2 * 91].size, 3)})
    #             temp['between'].update(
    #                 {data: round(df[data].loc[2 * 92:2 * 119].sum() / df[data].loc[2 * 92:2 * 119].size, 3)})
    #             temp['ding_2'].update(
    #                 {data: round(df[data].loc[2 * 120:2 * 271].sum() / df[data].loc[2 * 120:2 * 271].size, 3)})
    #             temp['after'].update(
    #                 {data: round(df[data].loc[2 * 271:].sum() / df[data].loc[2 * 271:].size, 3)})
    #     return temp

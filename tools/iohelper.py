import sys
from pathlib import Path
from os import path, makedirs
import logging

import pandas as pd


log = logging.getLogger(__name__)


class IOhelper:

    def __init__(self):
        """"""

    @staticmethod
    def reader(file):
        """
        Read file and create data frame
        :return: data_frame
        """
        try:
            with open(file, 'r') as f:
                data_frame = pd.read_csv(f, sep=' ')
        except IOError as error:
            log.error(error)
            sys.exit(1)
        else:
            if 'idle' not in data_frame.keys():
                log.error('Error: Use new BASH script')
                sys.exit(1)
        return data_frame

    @staticmethod
    def writer(file_name, figure, config=None):
        """
        This function create .html file with results

        :param file_name: Name of file will be created
        :param figure: Figure to file
        :param config: config for saving file
        :return:
        """
        abs_path = Path(__file__).parent.parent
        try:
            makedirs(f'{abs_path}/results', exist_ok=True)
        except OSError as error:
            log.error(f'Can\'t create directory, {error}')
            sys.exit(1)
        else:
            file_name = path.join(f'{abs_path}/results', f'{file_name}.html')
            try:
                with open(file_name, 'w') as f:
                    f.write(figure.to_html(config))
                    log.info(f'file saved in {file_name}')
            except IOError as error:
                log.error(f'Can\'t create file {error}')
                sys.exit(1)

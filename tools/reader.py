import sys

import pandas as pd


class Reader:

    def __init__(self, file):
        self.file = file

    def reader(self):
        """
        Read file and create  data frame
        :return: data_frame
        """
        try:
            with open(self.file, 'r') as f:
                data_frame = pd.read_csv(f, sep=' ')
        except IOError as error:
            print(error)
            sys.exit(1)
        else:
            if 'idle' not in data_frame.keys():
                print('Error: Use new BASH script')
                sys.exit(1)
        return data_frame

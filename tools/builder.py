from os import path, makedirs
import sys
import re

import pandas as pd
import plotly.graph_objects as go

from configs.settings import get_config, get_layout


class Builder:

    def __init__(self, files):
        self.files = files
        self.file_name = " VS ".join([file[file.rfind('/') + 1:] for file in self.files]).replace(".txt", "")

    def create_file(self):
        figures = list()

        for file in self.files:
            try:
                fw = re.search('-(.+?){3}-(.+?)-', file).group()[1:-1]
            except AttributeError as error:
                print(error)
                fw = file[file.rfind('/')+1:]
            data_frame = self.__reader(file)
            figures += self.__create_traces(data_frame, fw)

        fig_sub = go.Figure(data=figures, layout=get_layout(self.file_name))
        self.__writer(self.file_name, fig_sub, get_config(self.file_name))

    def __reader(self, file):
        try:
            with open(file, 'r') as f:
                data_frame = pd.read_csv(f, sep=' ')
        except IOError as error:
            print(error)
            sys.exit(1)
        else:
            if 'idle' not in data_frame.keys():
                print('Error: Use new BASH script')
                sys.exit(1)
        return data_frame

    def __writer(self, file_name, figure, config=None):
        try:
            makedirs("results", exist_ok=True)
        except OSError as error:
            print(error)
            sys.exit(1)
        else:
            file_name = path.join('results', f'{file_name}.html')
            try:
                with open(file_name, 'w') as f:
                    f.write(figure.to_html(config))
            except IOError as error:
                print(error)
                sys.exit(1)

    def __get_timestamp(self, data_frame):
        timestamp = list()
        start = 0
        for _ in range(len(data_frame)):
            timestamp.append(round(start, 1))
            start = start + 0.2
        return timestamp

    def __create_traces(self, data_frame, fw=""):
        traces = list()
        for data in data_frame:
            line = None
            if data == 'memory':
                line = dict(width=4, dash='solid')
            traces.append(
                go.Scatter(
                    x=self.__get_timestamp(data_frame),
                    y=data_frame[data],
                    mode='lines',
                    line=line,
                    name=f'{data} {fw}',
                )
            )
        return traces

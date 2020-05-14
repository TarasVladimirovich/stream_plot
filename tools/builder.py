from os import path, makedirs
import sys
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from configs.settings import get_config, get_layout
from tools.reader import Reader


class Builder:

    def __init__(self, files, artifacts=None, resources=None):
        self.files = files
        self.artifacts = artifacts
        self.resources = resources
        self.file_name = " VS ".join([file[file.rfind('/') + 1:] for file in self.files]).replace(".txt", "")

    def create_file(self):
        traces = list()

        for file in self.files:
            try:
                fw = re.search('-(.+?){3}-(.+?)-', file).group()[1:-1]
            except AttributeError as error:
                print(error)
                fw = file[file.rfind('/')+1:]
            data_frame = Reader(file).reader()
            traces += self.__create_traces(data_frame, fw)

        if self.artifacts is not None:
            self.__create_subplots(traces=traces)
        else:
            figure = go.Figure(data=traces, layout=get_layout(self.file_name))
            self.__writer(self.file_name, figure, get_config(self.file_name))

    def __reader(self, file):
        """
        Read file and create  data frame
        :param file: CSV file with headers
        :return: data_frame
        """
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
        """

        :param file_name: Name of file will be created
        :param figure: Figure to file
        :param config: config for saving file
        :return:
        """
        abs_path = Path(__file__).parent.parent
        try:
            makedirs(f'{abs_path}/results', exist_ok=True)
        except OSError as error:
            print(error)
            sys.exit(1)
        else:
            file_name = path.join(f'{abs_path}/results', f'{file_name}.html')
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
            visible = True
            if data == 'memory':
                line = dict(width=4, dash='solid')
            if data == 'sys':
                visible = 'legendonly'
            traces.append(
                go.Scatter(
                    visible=visible,
                    x=self.__get_timestamp(data_frame),
                    y=data_frame[data],
                    mode='lines',
                    line=line,
                    name=f'{data} {fw}',
                ),
            )
        return traces

    def __create_table(self, artifact):
        return go.Table(
            header=dict(
                values=["<b>Name</b>", "<b>Value</b>"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=12),
                align="left"
            ),
            cells=dict(
                values=[list(artifact.keys()), list(artifact.values())],
                line_color='darkslategray',
                fill_color='white',
                align="left",
                font=dict(color='darkslategray', size=12),
                height=20,
            )
        )

    def __create_table_resources(self, artifact):
        df = pd.DataFrame.from_dict(artifact)
        values = [''] + list(map(lambda p: f'<b>{p}</b>', list(df.columns)))
        values1 = [list(df.index)]
        print(values1)
        values1 += list(df[data] for data in df)
        print(df)
        return go.Table(
            header=dict(
                values=values,
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=12),
                align="left"
            ),
            cells=dict(
                values=values1,
                line_color='darkslategray',
                fill_color='white',
                align="left",
                font=dict(color='darkslategray', size=12),
                height=20,
            )
        )

    def __create_subplots(self, traces):
        fig_subplot = make_subplots(
            rows=2, cols=2,
            vertical_spacing=0.05,
            specs=[[{"type": "scatter", "colspan": 2}, None],
                   [{"type": "table"}, {"type": "table"}]
                   ]
        )

        for trace in traces:
            fig_subplot.add_trace(trace, col=1, row=1)

        fig_subplot.add_trace(self.__create_table(self.artifacts), row=2, col=1)
        fig_subplot.add_trace(self.__create_table_resources(self.resources), row=2, col=2)

        fig_subplot.update_layout(get_layout(self.file_name))
        fig_subplot.update_layout(height=1200)
        self.__writer(self.file_name, fig_subplot, get_config(self.file_name))


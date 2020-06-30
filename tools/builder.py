import re
import logging

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from configs.settings import get_config, get_layout
from tools.iohelper import IOhelper

logger = logging.getLogger(__name__)


class Builder:

    def __init__(self, files, artifacts=None, resources=None):
        self.files = files
        self.artifacts = artifacts
        self.resources = resources
        self.__file_name = None

    @property
    def file_name(self):

        if self.__file_name is None:

            if len(self.files) == 1:
                self.__file_name = self.files[0][self.files[0].rfind('/') + 1:].replace(".txt", "")
            else:
                self.__file_name = " VS ".join([file[file.rfind('/') + 1:]
                                                for file in self.files]).replace(".txt", "")
                to_delete = re.findall('(\d+-\d+-\d+T\d+_\d+_)', self.__file_name)
                for i in to_delete:
                    self.__file_name = self.__file_name.replace(i, "")

        return self.__file_name

    def create_file(self):

        traces = list()

        for file in self.files:
            try:
                fw = re.search('-([A-Z]){3}-(.+?)-', file).group()[1:-1]
            except AttributeError as error:
                logger.error(error)
                fw = file[file.rfind('/')+1:]
            data_frame = IOhelper().reader(file)
            traces += self.__create_traces(data_frame, fw)

        if self.artifacts is not None:
            self.__create_subplots(traces=traces)
        else:
            figure = go.Figure(data=traces, layout=get_layout(self.file_name[self.file_name.find('S'):]))
            IOhelper.writer(self.file_name, figure, get_config(self.file_name))

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

        fig_subplot.add_trace(self.__create_table_artifacts(self.artifacts), row=2, col=1)
        if self.resources is not None:
            fig_subplot.add_trace(self.__create_table_resources(self.resources), row=2, col=2)

        fig_subplot.update_layout(get_layout(self.file_name[self.file_name.find('S'):]))
        fig_subplot.update_layout(height=1200)
        IOhelper.writer(self.file_name, fig_subplot, get_config(self.file_name))

    def __get_timestamp(self, data_frame):
        timestamp = list()
        start = 0
        for _ in range(data_frame.size):
            timestamp.append(round(start, 1))
            start = start + 0.5
        return timestamp

    def __create_traces(self, data_frame, fw=""):
        hide = ['Ivaapp', 'PulseMem', 'sys']
        traces = list()
        for data in data_frame:
            line = None
            visible = True
            if 'Mem' in data:
                line = dict(width=4, dash='solid')
            if data in hide:
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

    def __create_table_artifacts(self, artifact):
        values_header = ["<b>Name</b>", "<b>Value</b>"]
        values_cells = [list(artifact.keys()), list(artifact.values())]
        return self.__create_table(values_header, values_cells)

    def __create_table_resources(self, artifact):
        df = pd.DataFrame.from_dict(artifact)
        values_header = [''] + list(map(lambda p: f'<b>{p}</b>', list(df.columns)))
        values_cells = [list(df.index)]
        values_cells.extend(list(df[data] for data in df))
        return self.__create_table(values_header, values_cells)

    def __create_table(self, header, cells):
        """
        Create table
        :param header: input List head
        :param cells: input List cells
        :return: Table
        """
        return go.Table(
            header=dict(
                values=header,
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=12),
                align="left"
            ),
            cells=dict(
                values=cells,
                line_color='darkslategray',
                fill_color='white',
                align="left",
                font=dict(color='darkslategray', size=12),
                height=20,
            )
        )

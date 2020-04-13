import os
import sys

import pandas as pd
import plotly.graph_objects as go


def reader(file):
    try:
        with open(file, 'r') as f:
            data = pd.read_csv(f, sep=' ')
    except IOError as error:
        print(error)
        sys.exit(1)
    return data


def writer(file_name, figure, config=None):
    try:
        os.makedirs("results", exist_ok=True)
    except OSError as error:
        print(error)
        sys.exit(1)
    else:
        file_name = os.path.join('results', f'{file_name}.html')
        try:
            with open(file_name, 'w') as f:
                f.write(figure.to_html(config))
        except IOError as error:
            print(error)
            sys.exit(1)


def get_timestamp(data_frame):
    timestamp = list()
    start = 0
    for _ in range(len(data_frame.idle)):
        timestamp.append(round(start, 1))
        start = start + 0.2
    return timestamp


def create_figure(data_frame, fw=""):
    traces = list()
    for data in data_frame:
        traces.append(
            go.Scatter(
                x=get_timestamp(data_frame),
                y=data_frame[data],
                mode='lines',
                name=f'{data} {fw}',
            )
        )
    return traces

import sys

import plotly.graph_objects as go

from settings import *


def main():
    result = reader(sys.argv[1])
    data = result['data']
    file_name = result['file_name'].replace(".txt", "")
    timestamp = get_timestamp(data)
    traces = list()
    for d in data:
        traces.append(
                     go.Scatter(
                                x=timestamp,
                                y=data[d],
                                mode='lines',
                                name=d,
                                )
                     )
    fig = go.Figure(data=traces, layout=get_layout(file_name))
    with open(f'{file_name}.html', 'w') as f:
        f.write(fig.to_html(get_config(file_name)))
    fig.to_html()


if __name__ == '__main__':
    main()

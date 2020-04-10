import pandas as pd


def get_layout(file_name):

    layout = dict(
                  title=file_name,
                  yaxis=dict({
                            'title': "CPU Usage",
                            }),
                  xaxis=dict({
                            'tickmode': 'array',
                            'tickvals': [30, 90, 120, 150, 270],
                            'title': "Time per 0.2 seconds",
                            }),
                  legend_title='<b> Processes </b>',
                  )

    return layout


def get_config(file_name):

    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'toImageButtonOptions': {
                                'format': 'jpeg',
                                'filename': file_name,
                                'height': 1000,
                                'width': 1400,
                                'scale': 1
                                },
        'modeBarButtonsToRemove': [
                                    'hoverClosestGl2d', 'hoverClosestPie', 'toggleHover', 'resetViews',
                                    'sendDataToCloud', 'toggleSpikelines', 'resetViewMapbox',
                                    'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo',
                                    'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', '2D'
                                    'zoom3d', 'pan3d', 'orbitRotation', 'tableRotation', 'handleDrag3d',
                                    'resetCameraDefault3d', 'resetCameraLastSave3d', 'hoverClosest3d'
                                    'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                                    ],

             }

    return config


def reader(file):
    with open(file, 'r') as f:
        data = pd.read_csv(f, sep=' ')
        file_name =f.name[f.name.rfind('/')+1:]
    return {'data': data, 'file_name': file_name}


def get_timestamp(data):
    timestamp = list()
    start = 0
    for _ in range(len(data.idle)):
        timestamp.append(round(start, 1))
        start = start + 0.2
    return timestamp

def get_layout(file_name):

    layout = dict(

                  width=1500,
                  height=800,
                  title={
                        'text': file_name,
                        'x': 0.5,
                        'y': 0.92,
                        'xanchor': 'center'
                        },
                  yaxis={
                        'title': "Percent, %",
                        },
                  xaxis={
                        'tickmode': 'array',
                        'tickvals': [30, 90, 120, 150, 270],
                        'title': "Time per 0.2 seconds",
                        'rangeslider': dict(
                                            visible=True
                                            ),
                        },
                  font={
                        'size': 8,
                        },
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


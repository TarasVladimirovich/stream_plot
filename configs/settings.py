def get_layout(file_name):

    layout = dict(
                  width=1600,
                  height=800,
                  title=dict(
                        text=f"<b>{file_name}<b>",
                        x=0.5,
                        y=0.92,
                        font=dict(
                                  size=20
                                 ),
                        xanchor='center',
                            ),
                  yaxis=dict(
                        title='Percent, %',
                  ),
                  xaxis=dict(
                        tickmode='array',
                        title='Time',
                        rangeslider=dict(
                                        visible=True,
                                        ),
                        ),
                  font=dict(
                        size=8,
                            ),
                  legend_title='<b> Processes </b>',
                  )

    return layout


def get_config(file_name):

    config = dict(
        displayModeBar=True,
        displaylogo=False,
        toImageButtonOptions=dict(
                                format='jpeg',
                                filename=file_name,
                                height=1000,
                                width=1400,
                                scale=1
                                ),
        modeBarButtonsToRemove=['hoverClosestGl2d', 'hoverClosestPie', 'toggleHover', 'resetViews',
                                'sendDataToCloud', 'toggleSpikelines', 'resetViewMapbox',
                                'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo',
                                'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', '2D'
                                'zoom3d', 'pan3d', 'orbitRotation', 'tableRotation', 'handleDrag3d',
                                'resetCameraDefault3d', 'resetCameraLastSave3d', 'hoverClosest3d'
                                'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                                ],
                 )

    return config


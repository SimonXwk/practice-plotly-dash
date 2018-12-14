import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
    csv_path = find_raw_csv_path('abalone.csv')

    df = pd.read_csv(csv_path)
    samples = {
        'A': np.random.choice(df['rings'], 30, replace=False),
        'B': np.random.choice(df['rings'], 20, replace=False)
    }

    boxpoints = request_arg('boxpoints', 'all', str, lambda x: x in ('all', 'outliers'))
    jitter = request_arg('jitter', 0.5, float, lambda x: 0 <= x <= 1)
    pointpos = request_arg('pointpos', -2, float, lambda x: -2 <= x <= 2)

    data = [
        go.Box(y=samples[sample], name=sample, boxpoints=boxpoints, jitter=jitter, pointpos=pointpos)
        for sample in samples
    ]

    layout = go.Layout(
        title="Sample of abalone rings values",
        yaxis={'title': 'Rings'},
        hovermode="x"
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

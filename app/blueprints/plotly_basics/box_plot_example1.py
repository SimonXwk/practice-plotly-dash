import plotly.graph_objs as go
import numpy as np
from app.data_source.csv import find_raw_csv_path
from app.helper import plot_div_to_example_html, request_arg


@plot_div_to_example_html
def draw():
    sample = np.random.randint(1, 1001, 200)    

    boxpoints = request_arg('boxpoints', 'all', str, lambda x: x in ('all', 'outliers'))
    jitter = request_arg('jitter', 0.5, float, lambda x: 0 <= x <=1)
    pointpos = request_arg('pointpos', -2, float, lambda x: -2 <= x <= 2)

    data = [go.Box(y=sample, name="sample data", boxpoints=boxpoints, jitter=jitter, pointpos=pointpos)]
    layout = go.Layout(title="Box Plot with numpy data sample",
                       yaxis={'title': 'Values'},
                       hovermode="x")
    fig = go.Figure(data=data, layout=layout)
    return fig

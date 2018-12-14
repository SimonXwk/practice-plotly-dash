import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
    csv_path = find_raw_csv_path('2018WinterOlympics.csv')

    df = pd.read_csv(csv_path)

    trace1 = go.Bar(x=df['NOC'], y=df['Gold'], name='Gold', marker={'color': '#FFFF00'})
    trace2 = go.Bar(x=df['NOC'], y=df['Silver'], name='Silver', marker={'color': '#A0A0A0'})
    trace3 = go.Bar(x=df['NOC'], y=df['Bronze'], name='Bronze', marker={'color': '#FF8000'})

    data = [trace1, trace2, trace3]

    barmode = request_arg('barmode', 'group', str, lambda x: x in ('group', 'stack', 'relative'))
    layout = go.Layout(title="Bar Chart 2018 Winter Olympics",
                        yaxis={'title': 'Number of Medals'},
                        barmode=barmode)

    fig = go.Figure(data=data, layout=layout)
    return fig

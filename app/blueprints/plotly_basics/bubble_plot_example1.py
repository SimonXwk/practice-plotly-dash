import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import plot_div_to_example_html


@plot_div_to_example_html
def draw():
    csv_path = find_raw_csv_path('mpg.csv')

    df = pd.read_csv(csv_path)
    # df = df[df.horsepower == '?']  # Bad Data Points Exists in Data Set

    max_bubble_size = 25
    min_value = df['weight'].min()
    max_value = df['weight'].max()
    bubble_size = ((df['weight'] - min_value) / (max_value - min_value + 1)) * max_bubble_size
    data = [go.Scatter(x=df['horsepower'],
                       y=df['mpg'],
                       text=df['name'],
                       mode="markers",
                       marker=dict(size=bubble_size,
                                   color=df['cylinders'],
                                   colorscale='Jet',
                                   showscale=True)
                       )]
    layout = go.Layout(title="MPG Bubble Chart",
                       xaxis={'title': 'horsepower'},
                       yaxis={'title': 'mpg'},
                       hovermode="closest")
    fig = go.Figure(data=data, layout=layout)
    return fig

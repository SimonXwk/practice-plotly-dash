import plotly.graph_objs as go
import numpy as np
from app.helper import plot_div_to_example_html


@plot_div_to_example_html
def draw():
  np.random.seed(42)  # set the seed (any number) to obtain the same points every time
  points = 100
  random_x = np.random.randint(1, 101, points)
  random_y = np.random.randint(1, 101, points)

  trace = go.Scatter(x=random_x,
                    y=random_y,
                    mode='markers',
                    marker={
                      'size': 12,
                      'color': 'rgb(0, 128, 255)',
                      'line': {
                        'width': 1
                      }
                    })

  data = [trace]

  layout = go.Layout(title="Scatter Chart Example",
                    xaxis={'title': 'X Axis'},
                    yaxis={'title': 'Y Axis'},
                    hovermode="closest"  # handles multiple points landing on the same vertical
                    )

  fig = go.Figure(data=data, layout=layout)
  return fig

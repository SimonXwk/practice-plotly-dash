import plotly.graph_objs as go
import numpy as np
from app.helper import single_plot_to_html_div


@single_plot_to_html_div
def draw():
  np.random.seed(56)
  points = 100
  x_values = np.linspace(0, 1, points)  # equal space numbers between 0 and 1 (stop value is included by default)
  y_values = np.random.randn(points)  # Random numbers with normal distribution

  trace0 = go.Scatter(x=x_values, y=y_values+5, mode="markers", name="series1")
  trace1 = go.Scatter(x=x_values, y=y_values+0, mode="lines", name="series2")
  trace2 = go.Scatter(x=x_values, y=y_values-5, mode="lines+markers", name="series3")

  data = [trace0, trace1, trace2]

  layout = go.Layout(title="Line Chart Example using Numpy")

  fig = go.Figure(data=data, layout=layout)
  return fig

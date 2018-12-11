import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import plot_div_to_example_html


@plot_div_to_example_html
def draw():
  fpath = find_raw_csv_path('nst-est2017-alldata.csv')

  df = pd.read_csv(fpath)

  df2 = df.loc[df['DIVISION'] == '1', :]
  df2.set_index('NAME', inplace=True)
  df2 = df2.loc[:, [col for col in df2.columns if col.startswith('POP')]]

  data = [go.Scatter(x=[col[-4:] for col in df2.columns], y=df2.loc[name, :], mode="lines+markers", name=name) for name in df2.index]
  layout = go.Layout(title="Line Chart Example using Pandas")
  fig = go.Figure(data=data, layout=layout)
  return fig
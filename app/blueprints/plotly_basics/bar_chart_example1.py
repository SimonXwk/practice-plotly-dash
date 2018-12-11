import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import plot_div_to_example_html
from flask import request


@plot_div_to_example_html
def draw():
  csv_path = find_raw_csv_path('2018WinterOlympics.csv')
  
  df = pd.read_csv(csv_path)

  trace1 = go.Bar(x=df['NOC'], y=df['Gold'], name='Gold', marker={'color': '#FFFF00'})
  trace2 = go.Bar(x=df['NOC'], y=df['Silver'], name='Silver', marker={'color': '#A0A0A0'})
  trace3 = go.Bar(x=df['NOC'], y=df['Bronze'], name='Bronze', marker={'color': '#FF8000'})

  data = [trace1, trace2, trace3]

  barmode = str(request.args.get('barmode')).strip()
  layout = go.Layout(title="Bar Chart 2018 Winter Olympics",
                      yaxis={'title': 'Number of Medals'},
                      barmode=barmode if  barmode in ('group', 'stack', 'relative') else 'group')

  fig = go.Figure(data=data, layout=layout)
  return fig
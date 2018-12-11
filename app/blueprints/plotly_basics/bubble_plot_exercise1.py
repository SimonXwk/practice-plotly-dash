#######
# Objective: Create a bubble chart that compares three other features
# from the mpg.csv dataset. Fields include: 'mpg', 'cylinders', 'displacement'
# 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'
######

# Perform imports here:
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import plot_div_to_example_html
from flask import request


@plot_div_to_example_html
def draw():
  # create a DataFrame from the .csv file:
  csv_path = find_raw_csv_path('.csv')

  df = pd.read_csv(csv_path)
  df.set_index(df.columns[0], inplace=True)
 
  # create traces using a list comprehension:
  data = [go.Bar(x=df.index, y=df.loc[:, col], name=col) for col in df.columns]

  # create a layout, remember to set the barmode here
  barmode = str(request.args.get('barmode')).strip()
  layout = go.Layout(title="Mocksurvey Result", 
                      yaxis={'title': 'Score'},
                      barmode=barmode if  barmode in ('group', 'stack', 'relative') else 'group')

  # create a fig from data & layout, and plot the fig.
  fig = go.Figure(data=data, layout=layout)
  return fig

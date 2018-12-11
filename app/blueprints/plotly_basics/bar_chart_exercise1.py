#######
# Objective: Create a stacked bar chart from
# the file ../data/mocksurvey.csv. Note that questions appear in
# the index (and should be used for the x-axis), while responses
# appear as column labels.  Extra Credit: make a horizontal bar chart!
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
  csv_path = find_raw_csv_path('mocksurvey.csv')

  df = pd.read_csv(csv_path, index_col=0)
  # df.set_index(df.columns[0], inplace=True)
 
  # create traces using a list comprehension:
  series = str(request.args.get('series')).strip()
  ori = str(request.args.get('orientation')).strip()
  ori = ori if ori in ('v', 'h') else 'v'
  if series == 'q':
    data = [go.Bar(x=df.columns if ori == 'v' else df.loc[idx, :], 
                    y=df.loc[idx, :] if ori == 'v' else df.columns, 
                    name=idx, orientation=ori) for idx in df.index]
  else:
    data = [go.Bar(x=df.index if ori == 'v' else df.loc[:, col],
                   y=df.loc[:, col] if ori == 'v' else df.index, 
                   name=col, orientation=ori) for col in df.columns]

  # create a layout, remember to set the barmode here
  barmode = str(request.args.get('barmode')).strip()
  layout = go.Layout(title="Mocksurvey Result", 
                      yaxis={'title': 'Response Score'} if ori == 'v' else None,
                      xaxis={'title': 'Response Score'} if ori == 'h' else None,
                      barmode=barmode if  barmode in ('group', 'stack', 'relative') else 'group')

  # create a fig from data & layout, and plot the fig.
  fig = go.Figure(data=data, layout=layout)
  return fig

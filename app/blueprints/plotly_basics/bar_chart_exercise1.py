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
from app.helper import plot_div_to_example_html, request_arg


@plot_div_to_example_html
def draw():
  # create a DataFrame from the .csv file:
  csv_path = find_raw_csv_path('mocksurvey.csv')

  df = pd.read_csv(csv_path, index_col=0)
  # df.set_index(df.columns[0], inplace=True)
 
  # create traces using a list comprehension:
  series = request_arg('series', 'q', str, lambda x: x in ('q', 'r'))
  ori = request_arg('orientation', 'v', str, lambda x: x in ('v', 'h'))

  if series == 'q':
    data = [go.Bar(x=df.columns if ori == 'v' else df.loc[idx, :], 
                    y=df.loc[idx, :] if ori == 'v' else df.columns, 
                    name=idx, orientation=ori) for idx in df.index]
  else:
    data = [go.Bar(x=df.index if ori == 'v' else df.loc[:, col],
                   y=df.loc[:, col] if ori == 'v' else df.index, 
                   name=col, orientation=ori) for col in df.columns]

  # create a layout, remember to set the barmode here
  barmode = request_arg('barmode', 'group', str, lambda x: x in ('group', 'stack', 'relative'))
  layout = go.Layout(title="Mocksurvey Result", 
                      yaxis={'title': 'Response Score'} if ori == 'v' else None,
                      xaxis={'title': 'Response Score'} if ori == 'h' else None,
                      barmode=barmode)

  # create a fig from data & layout, and plot the fig.
  fig = go.Figure(data=data, layout=layout)
  return fig

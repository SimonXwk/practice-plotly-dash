#######
# Objective: Using the file 2010YumaAZ.csv, develop a Line Chart
# that plots seven days worth of temperature data on one graph.
# You can use a for loop to assign each day to its own trace.
######

# Perform imports here:
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div


@single_plot_to_html_div
def draw():
  # Create a pandas DataFrame from 2010YumaAZ.csv
  csv_path = find_raw_csv_path('2010YumaAZ.csv')

  df = pd.read_csv(csv_path)

  # Use a for loop (or list comprehension to create traces for the data list)
  data = [go.Scatter(x=df.loc[df['DAY'] == weekday, 'LST_TIME'], y=df.loc[df['DAY'] == weekday, 'T_HR_AVG'], mode="lines+markers", name=weekday) for weekday in df['DAY'].unique()]

  # Define the layout
  layout = go.Layout(title="Daily temperature from June 1-7, 2010 in Yuma, Arizona")

  # Create a fig from data and layout, and plot the fig
  fig = go.Figure(data=data, layout=layout)
  return fig

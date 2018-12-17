#######
# Objective: Using the "flights" dataset available
# from the data folder as flights.csv
# create a heatmap with the following parameters:
# x-axis="year"
# y-axis="month"
# z-axis(color)="passengers"
######
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
	csv_path = find_raw_csv_path('flights.csv')
	df = pd.read_csv(csv_path)

	z_series = df['passengers']
	round_by = 5
	data = [go.Heatmap(
		y=df['month'],
		x=df['year'],
		z=z_series,
		name='passengers',
		colorscale='Portland',
		zmin=(int(z_series.min()/round_by)+1) * round_by,
		zmax=(int(z_series.max()/round_by)+1) * round_by
	)]

	layout = go.Layout(
		title="Passengers by flight Year & Month",
		yaxis={'title': 'month'},
		xaxis={'title': 'year'},
		hovermode="x"
	)

	fig = go.Figure(data=data, layout=layout)
	return fig

#######
# Objective: Create a histogram that plots the 'length' field
# from the Abalone dataset (../data/abalone.csv).
# Set the range from 0 to 1, with a bin size of 0.02
######
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
	csv_path = find_raw_csv_path('abalone.csv')

	# sex,length,diameter,height,whole_weight,shucked_weight,viscera_weight,shell_weight,rings
	df = pd.read_csv(csv_path)

	dim = 'length'
	x_series = df[dim]
	x_min, x_max = x_series.min(), x_series.max()

	size = request_arg('size', 0.02, int, lambda x: x in range(int(x_max+1)))

	data = [
		go.Histogram(
			x=x_series,
			xbins=dict(start=min(0, x_min), end=max(1, x_max), size=size),
		)
	]

	layout = go.Layout(
		title="abalone Histogram",
		yaxis={'title': dim},
		xaxis={'title': 'bins'},
		hovermode="x"
	)

	fig = go.Figure(data=data, layout=layout)
	return fig

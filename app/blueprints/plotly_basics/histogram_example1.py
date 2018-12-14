# a histogram displays an accurate representation of the overall distribution of a continuous feature
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
	csv_path = find_raw_csv_path('mpg.csv')
	df = pd.read_csv(csv_path)

	dim = 'mpg'
	x_series = df[dim]
	x_min, x_max = x_series.min(), x_series.max()

	size = request_arg('size', 2, int, lambda x: x in range(int(x_max+1)))

	data = [
		go.Histogram(
			x=x_series,
			xbins=dict(start=min(0, x_min), end=x_max, size=size),
		)
	]

	layout = go.Layout(
		title="MPG Histogram",
		yaxis={'title': dim},
		xaxis={'title': 'bins'},
		hovermode="x"
	)

	fig = go.Figure(data=data, layout=layout)
	return fig

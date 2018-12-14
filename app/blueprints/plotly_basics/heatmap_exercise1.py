import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():

	data = [
	]

	layout = go.Layout(
		title="Title",
		yaxis={'title': 'y'},
		xaxis={'title': 'x'},
		hovermode="x"
	)

	fig = go.Figure(data=data, layout=layout)
	return fig

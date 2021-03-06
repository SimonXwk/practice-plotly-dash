import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():
	data_sources = ['2010YumaAZ.csv', '2010SantaBarbaraCA.csv', '2010SitkaAK.csv']
	data_source = np.random.choice(data_sources)

	csv_path = find_raw_csv_path(data_source)
	df = pd.read_csv(csv_path)

	colorscales = [
		'Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
		'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
		'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis'
	]
	colorscale = np.random.choice(colorscales)
	data = [go.Heatmap(
		x=df['DAY'],
		y=df['LST_TIME'],
		z=df['T_HR_AVG'],
		colorscale=colorscale
	)]

	layout = go.Layout(
		title=f"{' '.join((data_source.rsplit('.', 1)[0][:4], data_source.rsplit('.', 1)[0][4:-2], data_source.rsplit('.', 1)[0][-2:]))} Temperature ({colorscale})",
		yaxis={'title': 'TIME'},
		xaxis={'title': 'WEEKDAY'},
		hovermode="x"
	)

	fig = go.Figure(data=data, layout=layout)
	return fig


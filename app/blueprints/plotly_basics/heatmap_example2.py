import plotly.graph_objs as go
from plotly import tools
import pandas as pd
import numpy as np
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div


@single_plot_to_html_div
def draw():
	data_sources = ['2010YumaAZ.csv', '2010SantaBarbaraCA.csv', '2010SitkaAK.csv']

	rows = 3
	cols = 1

	plot_height = 500
	vertical_spacing = 0.04

	fig = tools.make_subplots(
		rows=rows,
		cols=cols,
		start_cell='top-left',  # 'top-left', 'bottom-left'
		shared_yaxes=False,
		shared_xaxes=False,
		# specs=[[{}, {}, {}]],
		# vertical_spacing=vertical_spacing,
		# horizontal_spacing=0.001,
		subplot_titles=[' '.join((name.rsplit('.', 1)[0][:4], name.rsplit('.', 1)[0][4:-2], name.rsplit('.', 1)[0][-2:])) for name in data_sources]
	)

	dfs = []
	min_z = 0
	max_z = 0
	for index, data_source in enumerate(data_sources):
		df = pd.read_csv(find_raw_csv_path(data_source))
		dfs.append(df)
		min_z = df['T_HR_AVG'].min() if index == 0 else min(min_z, df['T_HR_AVG'].min())
		max_z = df['T_HR_AVG'].max() if index == 0 else max(max_z, df['T_HR_AVG'].max())

	round_by = 5
	min_z = (int(min_z/round_by) + 0) * round_by
	max_z = (int(max_z/round_by) + 1) * round_by

	colorscale = np.random.choice([
		'Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
		'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
		'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis'
	])

	data = [
		go.Heatmap(
			x=df['DAY'].map(lambda x: x[0:3]),
			y=df['LST_TIME'],
			z=df['T_HR_AVG'],
			colorscale=colorscale,
			name=data_sources[idx].rsplit('.', 1)[0][4:-2],
			zmin=min_z,
			zmax=max_z,
		)
		for idx, df in enumerate(dfs)
	]

	for index, trace in enumerate(data):
		fig.append_trace(trace, ((index+1) // (cols+1)) + 1, cols - ((index+1) % cols))

	fig.layout.update(
		# height=rows * plot_height + (rows + 1) * vertical_spacing,
		title=f"Temperature ({colorscale})",
	)

	return fig

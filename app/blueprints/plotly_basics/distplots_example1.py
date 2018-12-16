import plotly.figure_factory as ff
import numpy as np
import plotly.offline as pyo
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():

	num = request_arg('num', 200, int, lambda x: x > 0)

	hist_data = [np.random.randn(num)-x*2 for x in range(4)]
	group_labels = ['X' + str(x) for x in range(1, 5)]
	bins = [ 1. for _ in range(1, 5)]

	# FigureFactory.create_distplot requires scipy
	fig = ff.create_distplot(hist_data, 
		group_labels=group_labels,
		bin_size=bins, 
		curve_type='kde',   # 'kde' or 'normal'
		colors=None, 
		rug_text=None, 
		histnorm='probability density',  # 'probability density' or 'probability'
		show_hist=True, show_curve=True, show_rug=True
	)
	return fig

from app.blueprints import MyBlueprint
import plotly.offline as pyo
import os

bp = MyBlueprint('plotly_basic', __name__)


def plot_offline(figure):
	pyo.plot(figure, filename=bp.offline_temp_html)


def get_data_file_path(filename=None):
	base_path = bp.blueprint.root_path.rsplit(os.sep, 2)[0]
	return os.path.join(base_path, 'data_source', filename)

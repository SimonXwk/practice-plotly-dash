from werkzeug.utils import find_modules, import_string
from flask import Blueprint
import os


class MyBlueprint(object):
	def __init__(self, blueprint_name, import_name, has_url_prefix=True, **options):
		self.blueprint = Blueprint(blueprint_name, import_name, static_folder='static', template_folder='templates', url_prefix='/' + blueprint_name if has_url_prefix else '', **options)
		self.offline_temp_html = os.path.join(self.blueprint.root_path, self.blueprint.template_folder , 'temp.html')

	def plot_offline(self, figure):
		import plotly.offline as pyo
		pyo.plot(figure, filename=self.offline_temp_html)

	def get_data(self, filename=None):
		base_path = self.blueprint.root_path.rsplit(os.sep, 2)[0]
		print(base_path)
		return os.path.join(base_path, 'data', filename)


# Circular import in Blueprint is not allowed for this method
def get_blueprint_objects(blueprint_obj_name='bp', **kwargs):
	blueprint_package_path_string = __name__
	print(f' * Registering Blueprint Objects named "{blueprint_obj_name}" in package "{blueprint_package_path_string}"')
	for dotted_module_name in find_modules(blueprint_package_path_string, **kwargs):
		module = import_string(dotted_module_name, silent=False)
		print(f' ? Searching : /{dotted_module_name}/')
		if hasattr(module, blueprint_obj_name):
			bp = import_string(':'.join((dotted_module_name, blueprint_obj_name)))
			bp = bp.blueprint
			if isinstance(bp, Blueprint):
				print(f'   ["{blueprint_obj_name}"] object {bp} found - [name: {bp.name}]')
				yield bp
		else:
			print(f' - ["{blueprint_obj_name}" ???] can not be found !')


def register_blueprints(app, blueprint_obj_name='bp', **kwargs):
	print('-' * 100)
	for blueprint in get_blueprint_objects(blueprint_obj_name=blueprint_obj_name, **kwargs):
		app.register_blueprint(blueprint)
		print(f' + Registration Successful : <{blueprint.name}>')
	print('-' * 100)

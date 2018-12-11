from werkzeug.utils import find_modules, import_string
from flask import Blueprint
import os
from app.helper import LazyLoad


class MyBlueprint(object):
	def __init__(self, blueprint_name, import_name, has_url_prefix=True, **options):
		self.blueprint = Blueprint(blueprint_name, import_name, static_folder='static', template_folder='templates', url_prefix='/' + blueprint_name if has_url_prefix else '', **options)
		self.static_folder_path = os.path.join(self.blueprint.root_path, self.blueprint.static_folder)

	def lazy_load_view_func(self, import_name):
		string_to_import = '.'.join((self.blueprint.import_name, import_name))
		return LazyLoad(string_to_import)

	def add_url(self, import_name, url_rules=None, **options):
		url_rules = [] if url_rules is None else url_rules
		lazy_loader = self.lazy_load_view_func(import_name)
		for url_rule in url_rules:
			self.blueprint.add_url_rule(url_rule, view_func=lazy_loader, **options)

	def add_filter(self, import_name, filter_name):
		lazy_loader = self.lazy_load_view_func(import_name)
		self.blueprint.add_app_template_filter(lazy_loader, name=filter_name)

	def add_test(self, import_name, test_name):
		lazy_loader = self.lazy_load_view_func(import_name)
		self.blueprint.add_app_template_test(lazy_loader, name=test_name)


# Circular import in Blueprint is not allowed for this method
def get_blueprint_objects(blueprint_obj_name='bp', **kwargs):
	blueprint_package_path_string = __name__
	print(f' * Searching in package "{blueprint_package_path_string}"')
	for dotted_module_name in find_modules(blueprint_package_path_string, **kwargs):
		module = import_string(dotted_module_name, silent=False)
		print(f'   Looking for attribute "{blueprint_obj_name}" in module /{dotted_module_name}/')
		if hasattr(module, blueprint_obj_name):
			bp = import_string(':'.join((dotted_module_name, blueprint_obj_name)))
			bp = bp.blueprint
			if isinstance(bp, Blueprint):
				print(f'   Found Blueprint {bp} - [name: {bp.name}]')
				yield bp
		else:
			print(f' - ["{blueprint_obj_name}" ???] can not be found !')


def register_blueprints(app, blueprint_obj_name='bp', **kwargs):
	print('-' * 100)
	print(f' * Registering Blueprints to {app}')
	for blueprint in get_blueprint_objects(blueprint_obj_name=blueprint_obj_name, **kwargs):
		app.register_blueprint(blueprint)
		print(f' + <{blueprint.name}>')
	print('-' * 100)

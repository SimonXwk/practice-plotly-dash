from flask import Flask
from app.blueprints import register_blueprints


def create_app():
	import_name = __name__.split('.')[0]
	server = Flask(import_name)

	with server.app_context():
		register_blueprints(server,  blueprint_obj_name='bp', include_packages=True, recursive=False)

	return server

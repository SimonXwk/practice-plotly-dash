from flask import Flask
from app.blueprints import register_blueprints


def create_app():
	import_name = __name__.split('.')[0]
	server = Flask(import_name)

	# Stop Jinja2 from keeping white spaces
	server.jinja_env.trim_blocks = True
	server.jinja_env.lstrip_blocks = True

	with server.app_context():
		register_blueprints(server,  blueprint_obj_name='bp', include_packages=True, recursive=False)

	return server

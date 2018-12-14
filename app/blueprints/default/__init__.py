from app.blueprints import MyBlueprint
from flask import send_from_directory
import os

view_funcs_list = (
	dict(import_name='view_funcs.root_view_handler', url_rules=['/'], endpoint='index'),
	dict(import_name='favicon_handler', url_rules=['/favicon.ico']),
)
bp = MyBlueprint(__name__, url_rules=view_funcs_list, has_url_prefix=False)


def favicon_handler():
	return send_from_directory(os.path.join(bp.root_path, bp.static_folder), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

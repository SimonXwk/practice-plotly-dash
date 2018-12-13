from app.blueprints import MyBlueprint
from flask import send_from_directory

bp = MyBlueprint(__name__, has_url_prefix=False)

view_funcs_list = (
	dict(import_name='view_funcs.root_view_handler', url_rules=['/'], endpoint='index'),
	dict(import_name='favicon_handler', url_rules=['/favicon.ico']),
)

# Add URL rules to the blueprint ( a wrapper around .add_url_rule() function )
bp.register_urls(view_funcs_list)


def favicon_handler():
	return send_from_directory(bp.static_folder_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

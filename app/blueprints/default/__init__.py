from app.blueprints import MyBlueprint
from flask import send_from_directory

bp = MyBlueprint('default', __name__, has_url_prefix=False)

# Add URL rules to the blueprint ( a wrapper around .add_url_rule() function )
bp.add_url('favicon_handler', ['/favicon.ico'])
bp.add_url('view_funcs.root_view_handler', ['/'])


def favicon_handler():
	return send_from_directory(bp.static_folder_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

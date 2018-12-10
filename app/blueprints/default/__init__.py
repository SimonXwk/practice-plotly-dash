from app.blueprints import MyBlueprint
from app.helper import templatified
from flask import send_from_directory
import os

bp = MyBlueprint('default', __name__, has_url_prefix=False)


@bp.blueprint.route("/favicon.ico")
def favicon_handler():
	return send_from_directory(bp.static_folder_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.blueprint.route("/")
@templatified('index', title="Home")
def root_view_handler():
	return None

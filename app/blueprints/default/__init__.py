from app.blueprints import MyBlueprint
from app.helper import templatified

bp = MyBlueprint('default', __name__, has_url_prefix=False)


@bp.blueprint.route("/")
@templatified('index', title="Home")
def root_view_handler():
	return None

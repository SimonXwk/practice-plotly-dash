from app.blueprints import MyBlueprint
from app.helper import apply_template

view_funcs_list = (
	dict(import_name='index', url_rules=['/'], endpoint='index'),
)
bp = MyBlueprint(__name__, url_rules=view_funcs_list)


@apply_template('example', 'Dash')
def index():
	return dict(
		endpoints=('.'.join((bp.name, item['endpoint'] if item.get('endpoint', False) else item['import_name'])) for item in view_funcs_list)
	)
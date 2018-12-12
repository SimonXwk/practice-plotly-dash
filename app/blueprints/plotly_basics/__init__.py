from app.blueprints import MyBlueprint
from app.helper import apply_template

bp = MyBlueprint('plotly_basics', __name__)

view_funcs_list = (
	dict(import_name='index', url_rules=['/'], endpoint='index'),
	dict(import_name='scatter_plot_example1.draw', url_rules=['/scatter1'], endpoint='scatter1'),
	dict(import_name='line_chart_example1.draw', url_rules=['/line1'], endpoint='line1'),
	dict(import_name='line_chart_example2.draw', url_rules=['/line2'], endpoint='line2'),
	dict(import_name='line_chart_exercise.draw', url_rules=['/line3'], endpoint='line3'),
	dict(import_name='bar_chart_example1.draw', url_rules=['/bar1'], endpoint='bar1'),
	dict(import_name='bar_chart_exercise1.draw', url_rules=['/bar2'], endpoint='bar2'),
	dict(import_name='bubble_plot_example1.draw', url_rules=['/bubble1'], endpoint='bubble1'),
	dict(import_name='bubble_plot_exercise1.draw', url_rules=['/bubble2'], endpoint='bubble2'),
)

bp.register_urls(view_funcs_list)


@apply_template('example', 'Plotly Basic Plots')
def index():
	return dict(
		endpoints=('.'.join((bp.blueprint.name, item['endpoint'] if item.get('endpoint', False) else item['import_name'])) for item in view_funcs_list)
	)


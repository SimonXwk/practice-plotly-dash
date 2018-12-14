from app.blueprints import MyBlueprint
from app.helper import apply_template

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
	dict(import_name='box_plot_example1.draw', url_rules=['/box1'], endpoint='box1'),
	dict(import_name='box_plot_example2.draw', url_rules=['/box2'], endpoint='box2'),
	dict(import_name='box_plot_exercise1.draw', url_rules=['/box3'], endpoint='box3'),
	dict(import_name='histogram_example1.draw', url_rules=['/hist1'], endpoint='hist1'),
	dict(import_name='histogram_exercise1.draw', url_rules=['/hist2'], endpoint='hist2'),
	dict(import_name='distplots_example1.draw', url_rules=['/distp1'], endpoint='distp1'),
	dict(import_name='distplots_exercise1.draw', url_rules=['/distp2'], endpoint='distp2'),
	dict(import_name='heatmap_example1.draw', url_rules=['/heat1'], endpoint='heat1'),
	dict(import_name='heatmap_exercise1.draw', url_rules=['/heat2'], endpoint='heat2'),

)
bp = MyBlueprint(__name__, url_rules=view_funcs_list)


@apply_template('example', 'Plotly Basic Plots')
def index():
	return dict(
		endpoints=('.'.join((bp.name, item['endpoint'] if item.get('endpoint', False) else item['import_name'])) for item in view_funcs_list)
	)


from app.blueprints import MyBlueprint

bp = MyBlueprint('plotly_basics', __name__)

bp.add_url('scatter_plot_example1.draw', ['/scatter1'], endpoint='scatter1')
bp.add_url('line_chart_example1.draw', ['/line1'], endpoint='line1')
bp.add_url('line_chart_example2.draw', ['/line2'], endpoint='line2')
bp.add_url('line_chart_exercise.draw', ['/line3'], endpoint='line3')
bp.add_url('bar_chart_example1.draw', ['/bar1'], endpoint='bar1')
bp.add_url('bar_chart_exercise1.draw', ['/bar2'], endpoint='bar2')
bp.add_url('bubble_plot_example1.draw', ['/bubble1'], endpoint='bubble1')
bp.add_url('bubble_plot_exercise1.draw', ['/bubble2'], endpoint='bubble2')

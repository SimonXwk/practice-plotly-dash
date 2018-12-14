#######
# This plot compares sample distributions
# of three-letter-words in the works of
# Quintus Curtius Snodgrass and Mark Twain
######
import plotly.graph_objs as go
from app.helper import single_plot_to_html_div, request_arg
from app.func_map import fm


@single_plot_to_html_div
@fm.register(('/aaa', '/bbb'))
def draw():
    compare = {
        'snodgrass': [.209,.205,.196,.210,.202,.207,.224,.223,.220,.201],
        'twain': [.225,.262,.217,.240,.230,.229,.235,.217]
    }
   
    boxpoints = request_arg('boxpoints', 'outliers', str, lambda x: x in ('all', 'outliers'))
    jitter = request_arg('jitter', 0.5, float, lambda x: 0 <= x <=1)
    pointpos = request_arg('pointpos', -2, float, lambda x: -2 <= x <= 2)

    data = [go.Box(y=compare[c], name=c, boxpoints=boxpoints, jitter=jitter, pointpos=pointpos) for c in compare]
    layout = go.Layout(title="The Case of Mark Twain & Snodgrass",
                       yaxis={'title': 'Frequency'},
                       hovermode="x"
                       )
    fig = go.Figure(data=data, layout=layout)
    return fig

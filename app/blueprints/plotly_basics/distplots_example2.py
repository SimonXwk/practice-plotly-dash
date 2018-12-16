import plotly.figure_factory as ff
from app.helper import single_plot_to_html_div


@single_plot_to_html_div
def draw():
    compare = {
        'snodgrass': [.209, .205, .196, .210, .202, .207, .224, .223, .220, .201],
        'twain': [.225, .262, .217, .240, .230, .229, .235, .217]
    }

    hist_data = tuple(compare.values())
    group_labels = tuple(compare.keys())
    bins = [ 0.005 for _ in range(len(compare))]

    # FigureFactory.create_distplot requires scipy
    fig = ff.create_distplot(hist_data, 
        group_labels=group_labels,
        bin_size=bins, 
        curve_type='kde',  # 'kde' or 'normal'
        colors=None, 
        rug_text=None, 
        histnorm='probability density',  # 'probability density' or 'probability'
        show_hist=True, show_curve=True, show_rug=True
    )

    return fig

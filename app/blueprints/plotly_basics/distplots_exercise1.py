#######
# Objective: Using the iris dataset, develop a Distplot
# that compares the petal lengths of each class.
# File: '../data/iris.csv'
# Fields: 'sepal_length','sepal_width','petal_length','petal_width','class'
# Classes: 'Iris-setosa','Iris-versicolor','Iris-virginica'
######
import plotly.figure_factory as ff
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div, request_arg


@single_plot_to_html_div
def draw():

    csv_path = find_raw_csv_path('iris.csv')
    df = pd.read_csv(csv_path)

    dim = 'petal_length'
    classes = df['class'].unique()

    hist_data = [df[df['class'] == c][dim] for c in classes]
    group_labels = classes
    bins = [1 for c in classes]

    fig = ff.create_distplot(hist_data, 
        group_labels=group_labels,
        bin_size=bins, 
        curve_type='kde',  # 'kde' or 'normal'
        colors=None, 
        rug_text=None, 
        histnorm='probability density',  # 'probability density' or 'probability'
        show_hist=True, show_curve=True, show_rug=True
    )
    fig.layout.title = dim.title()
    return fig

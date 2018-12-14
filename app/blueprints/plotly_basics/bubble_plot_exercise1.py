#######
# Objective: Create a bubble chart that compares three other features
# from the mpg.csv dataset. Fields include: 'mpg', 'cylinders', 'displacement'
# 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'
######

# Perform imports here:
import plotly.graph_objs as go
import pandas as pd
from app.data_source.csv import find_raw_csv_path
from app.helper import single_plot_to_html_div


@single_plot_to_html_div
def draw():
    # create a DataFrame from the .csv file:
    csv_path = find_raw_csv_path('mpg.csv')

    df = pd.read_csv(csv_path)

    max_bubble_size = 30
    bubble_size_dimension = 'horsepower'

    df[bubble_size_dimension] = pd.to_numeric(df[bubble_size_dimension], errors='coerce')  # Convert to numbers

    min_value = df[bubble_size_dimension].min()
    max_value = df[bubble_size_dimension].max()

    df[bubble_size_dimension] = df[bubble_size_dimension].fillna(min_value)  # Fill All NaN with min value (Not Zero, otherwise the min size will be too small)
    bubble_size = ((df[bubble_size_dimension] - min_value) / (max_value - min_value + 1)) * max_bubble_size

    x_dimension = 'displacement'
    y_dimension = 'acceleration'
    color_dimension = 'model_year'
    text_dimension = 'name'

    # create traces using a list comprehension:
    data = [go.Scatter(x=df[x_dimension],
                       y=df[y_dimension],
                       text=df[text_dimension].str.title(),
                       name="mpg data",
                       mode="markers",
                       marker=dict(size=bubble_size,
                                   color=df[color_dimension],
                                   showscale=True)
                       )]

    # create a layout, remember to set the barmode here
    layout = go.Layout(title=f"MPG {x_dimension.title()} & {y_dimension.title()}",
                       xaxis={'title': x_dimension},
                       yaxis={'title': y_dimension},
                       hovermode="closest"
                       )

    # create a fig from data & layout, and plot the fig.
    fig = go.Figure(data=data, layout=layout)
    return fig

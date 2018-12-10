import pandas as pd
import plotly.graph_objs as go
from app.blueprints.plotly_basics import bp

fpath = bp.get_data('nst-est2017-alldata.csv')
df = pd.read_csv(fpath)
print(df.head())


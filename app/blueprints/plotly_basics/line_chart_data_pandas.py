import pandas as pd
import plotly.graph_objs as go
from . import plot_offline, get_data_file_path

fpath = get_data_file_path('nst-est2017-alldata.csv')
df = pd.read_csv(fpath)
print(df.head())
df2 = df[df['DIVISION'] == 1]
df2.set_index('NAME', inplace=True)
df2 = df2[[col for col in df2.columns if col.startswith('POP')]]

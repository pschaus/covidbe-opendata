import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

start = '03-01'

df = pd.read_csv(f'static/csv/MAPS.csv', header=None, names=["date", "value"])
mask = (df['date'] >= f'{2020}-{start}')
df = df.loc[mask]
df['date'] = pd.to_datetime(df['date'])
df.reset_index(level=0, inplace=True)
df.set_index('date', inplace=True)
df = df.between_time('08:00', '08:00')
df = df[df.index.dayofweek < 5]
df.reset_index(level=0, inplace=True)




@register_plot_for_embedding("gooole_traffic_working_days")
def plot_google_traffic_working_days():
    """
    google traffic working days
    """

    fig = px.scatter(df, x='date', y='value',
                     labels={'date': 'date', 'value': 'google MAP traffic BE working days 8:00AM'})

    return fig



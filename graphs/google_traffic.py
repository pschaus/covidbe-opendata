import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

start = '03-01'


countries = ['BE','FR','DE','NL']

def get_df(country):
    df = pd.read_csv(f'static/csv/traffic/{country}/MAPS.csv',parse_dates = ['date'])
    df.reset_index(level=0, inplace=True)
    df.set_index('date', inplace=True)
    df = df.between_time('08:00', '08:00')
    df = df[df.index.dayofweek < 5]
    df.reset_index(level=0, inplace=True)
    tot = df['value'].sum()
    df['value'] =df['value']/tot
    return df

dfmap = {c:get_df(c) for c in countries}



@register_plot_for_embedding("gooole_traffic_working_days")
def plot_google_traffic_working_days():
    """
    google traffic working days
    """
    fig = go.Figure()
    for c in countries:
        df = dfmap[c]
        fig.add_trace(go.Scatter(x=df.date, y=df.value, mode='lines', name=c))

    fig.update_layout(
        title="Normalized google map traffic 8:00-8:30 workdays",
        xaxis_title="day",
        yaxis_title="normalized traffic"
    )
    return fig



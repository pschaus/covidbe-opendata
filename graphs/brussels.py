

from graphs import register_plot_for_embedding

import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext


import plotly.express as px


df = pd.read_csv(f'static/csv/tunnels_bxl.csv',parse_dates = ['from','to'])
mask = (df['from'] > '2020-03-1')
df = df.loc[mask]
df.reset_index(level=0, inplace=True)
df.set_index('from', inplace=True)


def fig_tunnel(weekday=True,time='07:00'):
    df_ = df.between_time(time,time)
    if weekday:
        df_ = df_[df_.index.dayofweek < 5]
    else:
        df_ = df_[df_.index.dayofweek == 5]
    df_.reset_index(level=0, inplace=True)

    fig = px.line(df_, x="from", y="volume", color="tunnel")

    fig.update_layout(
            xaxis_title="day",
            yaxis_title="#vehicles"
    )
    return fig

@register_plot_for_embedding("brussels-tunnels")
def brussels_tunnels():
    fig1 = fig_tunnel(True, '07:00')
    fig1.update_layout(title="#Tunnel Traffic of Brussels at 8:00-9:00 Workdays")
    return fig1
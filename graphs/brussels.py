

from graphs import register_plot_for_embedding

import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext

from datetime import datetime
import plotly.express as px



mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M")

df = pd.read_csv(f'static/csv/tunnels_bxl.csv',parse_dates = ['from','to'],date_parser=mydateparser)



mask = (df['from'] >= '2020-02-1')
df = df.loc[mask]

mask = (df['from'] <= '2020-05-19')
df = df.loc[mask]


df.sort_values(by='from',inplace=True)



df.reset_index(level=0, inplace=True)
df.set_index('from', inplace=True)


def fig_tunnel(weekday=True, time='07:00'):
    df_ = df.between_time(time, time)
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


def fig_tunnel_ratio(weekday=True, time='07:00'):
    df_ = df.between_time(time, time)
    if weekday:
        df_ = df_[df_.index.dayofweek < 5]
    else:
        df_ = df_[df_.index.dayofweek == 5]
    df_.reset_index(level=0, inplace=True)

    mask = (df_['from'] <= '2020-03-10')
    df2 = df_.loc[mask]

    df2 = df2.groupby('tunnel').mean()

    dict_mean = df2.to_dict()['volume']

    df_['rel_volume'] = df_.apply(lambda row: row['volume'] / dict_mean[row['tunnel']], axis=1)

    fig = px.line(df_, x="from", y="rel_volume", color="tunnel")

    fig.update_layout(
        xaxis_title="day",
        yaxis_title="ratio wrt to normality"
    )
    return fig


@register_plot_for_embedding("brussels-tunnels")
def brussels_tunnels():
    fig1 = fig_tunnel(True, '07:00')
    fig1.update_layout(title="#Tunnel Traffic of Brussels at 7:00-8:00 Workdays")
    return fig1


@register_plot_for_embedding("brussels-tunnels-ratio")
def brussels_tunnels_ratio():
    fig1 = fig_tunnel_ratio(True, '07:00')
    fig1.update_layout(title="#Tunnel Traffic of Brussels at 7:00-8:00 Workdays")
    return fig1
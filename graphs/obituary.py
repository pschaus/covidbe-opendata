import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import urllib.request, json

from graphs import register_plot_for_embedding


@register_plot_for_embedding("sud_presse")
def sud_presse():
    df_sp = pd.read_csv(f'static/csv/necrosudpresse.csv')
    df_sp = df_sp.groupby(['date']).size().reset_index(name='counts')
    line = go.Scatter(
            x=df_sp.date,
            y=df_sp.counts.rolling(7).mean(),
            mode='lines',
        )
    fig = go.Figure(data=[line], )
    fig.update_layout(template="plotly_white",title="Obituary data from http://necro.sudpresse.be")
    return fig

@register_plot_for_embedding("dansnospensees")
def dans_nos_pensees():
    df_dp = pd.read_csv(f'static/csv/dansnopensees.csv')
    df_dp = df_dp.groupby(['date']).size().reset_index(name='counts')
    line = go.Scatter(
            x=df_dp.date,
            y=df_dp.counts.rolling(7).mean(),
            mode='lines',
        )
    fig = go.Figure(data=[line], )
    fig.update_layout(template="plotly_white",title="Obituary data from www.dansnospensees.be")
    return fig


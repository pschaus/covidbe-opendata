import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
from graphs import register_plot_for_embedding

import numpy as np
import altair as alt
from pages import get_translation


from datetime import datetime

import pandas
import geopandas


df=pd.read_csv('static/csv/be-covid-vaccines.csv') # last line is NaN

df_A = df[df.DOSE == 'A']
df_B = df[df.DOSE == 'B']

df_A = df_A.groupby(['DATE']).agg({'COUNT': 'sum'})
df_B = df_B.groupby(['DATE']).agg({'COUNT': 'sum'})

@register_plot_for_embedding("vaccines_daily")
def plot_vaccines_cumulated():
    """
    plot of the cumulated vaccines
    """
    fig = make_subplots(specs=[[{"secondary_y": True, }]], shared_yaxes='all', shared_xaxes='all')

    fig.add_trace(
        go.Scatter(x=df_A.index, y=df_A.COUNT.cumsum(), name=gettext('Cumulated DOSE A')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_B.index, y=df_B.COUNT.cumsum(), name=gettext('Cumulated DOSE B')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=df_A.index, y=df_A.COUNT, name=gettext('Daily DOSE A')),
        secondary_y=True,
    )

    fig.add_trace(
        go.Bar(x=df_B.index, y=df_B.COUNT, name=gettext('Daily DOSE B')),
        secondary_y=True,
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="Cumulated", secondary_y=False)
    fig.update_yaxes(title_text="Daily", secondary_y=True)

    fig.update_layout(title=gettext("Vaccines Belgium"))
    fig.update_layout(template="plotly_white")
    fig.update_layout(yaxis_range=[0, max(df_A.COUNT.cumsum().values)])
    return fig
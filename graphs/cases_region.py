import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np


from graphs import register_plot_for_embedding

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np
import io
import requests
from graphs import register_plot_for_embedding

df = pd.read_csv('static/csv/be-covid-provinces-all.csv')

df = df.groupby([df.DATE, df.REGION]).agg(
    {'CASES': ['sum'], 'TESTS_ALL': ['sum'], 'TESTS_ALL_POS': ['sum']}).reset_index()
df.columns = df.columns.get_level_values(0)


def moving_average(a, n=1):
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n - 1] = ret[:n - 1] / range(1, n)
    ret[n - 1:] = ret[n - 1:] / n
    return ret


def trace(region, log=False, div=1, mul=1):
    return go.Scatter(name=region,
                      x=df[df.REGION == region].DATE,
                      y=moving_average(df[df.REGION == region].CASES.values, 7) / div * mul)


def plot_absolute_cases():
    fig = go.Figure()
    fig.add_trace(trace('Wallonia'))
    fig.add_trace(trace('Flanders'))
    fig.add_trace(trace('Brussels'))
    # fig.update_yaxes(type="log")
    fig.update_layout(template="plotly_white", title="Number of cases")
    return fig


def plot_relative_cases():
    fig = go.Figure()
    brux_pop = 1218255
    wall_pop = 3645243
    flanders_pop = 6629143

    fig.add_trace(trace('Wallonia', div=wall_pop, mul=100000))
    fig.add_trace(trace('Flanders', div=flanders_pop, mul=100000))
    fig.add_trace(trace('Brussels', div=brux_pop, mul=100000))

    fig.update_layout(template="plotly_white", title="Number of cases/100000 habitants")
    return fig


def cases_absolute_region():
    return plot_absolute_cases()

def cases_relative_region():
    return plot_relative_cases()

def cases_absolute_region():
    return plot_absolute_cases()

def cases_absolute_region_log():
    fig = plot_absolute_cases()
    fig.update_yaxes(type="log")
    return fig

def cases_relative_region_log():
    fig = plot_relative_cases()
    fig.update_yaxes(type="log")
    return fig
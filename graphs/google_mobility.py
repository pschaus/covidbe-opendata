import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from graphs import register_plot_for_embedding
import urllib.request, json
import geopandas
from unidecode import unidecode

from datetime import datetime, date
import numpy as np
from flask_babel import gettext

countries = ['BE', 'FR', 'NL', 'DE', 'LU', 'GB', 'PT', 'SP', 'IT', 'SE']  # , 'PL'

df = pd.read_csv(f'static/csv/google_mobility_report_eu.csv', parse_dates=['date'])

dfmap = {c: df[df['country_region_code'] == c] for c in countries}

graphs = ['workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline',
          'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
          'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', ]


def moving_average(a, n=1):
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n - 1] = ret[:n - 1] / range(1, n)
    ret[n - 1:] = ret[n - 1:] / n
    return ret


@register_plot_for_embedding("google_mobility_plot_eu")
def google_mobility_plot_eu():
    colors = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'  # blue-teal
    ]
    large_fig = make_subplots(rows=len(graphs), cols=1, subplot_titles=graphs, horizontal_spacing=0.05,
                              vertical_spacing=0.02, shared_xaxes=True)
    r = 1
    for g in graphs:

        fig = go.Figure()
        a = 0
        for c in countries:
            df = dfmap[c]
            values = df[g].values
            if len(values) > 0:
                values = np.nan_to_num(values)
                values = moving_average(values, 7)

                large_fig.append_trace(
                    go.Scatter(x=df.date, y=values, line=dict(color=colors[a]), mode='lines', name=c, legendgroup=c,
                               showlegend=(r == 1)), row=r, col=1)

            a += 1

        r += 1
    large_fig['layout'].update(height=1500, title='Google Mobility Reports (7 day average)')
    large_fig.update_layout(template="plotly_white")
    return large_fig


subregion = ['Antwerp', 'East Flanders', 'Flemish Brabant', 'Limburg', 'West Flanders', 'Hainaut', 'Liege', 'Luxembourg', 'Province of Namur', 'Walloon Brabant',]
df_be = pd.read_csv(f'static/csv/google_mobility_report_be.csv', parse_dates=['date'])
dfmapbe = {c: df_be[df_be['sub_region_2'] == c] for c in subregion}


@register_plot_for_embedding("google_mobility_plot_be")
def google_mobility_plot_be():
    colors = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'  # blue-teal
    ]
    large_fig = make_subplots(rows=len(graphs), cols=1, subplot_titles=graphs, horizontal_spacing=0.05,
                              vertical_spacing=0.02, shared_xaxes=True)
    r = 1
    for g in graphs:

        fig = go.Figure()
        a = 0
        for c in subregion:
            df = dfmapbe[c]
            values = df[g].values
            if len(values) > 0:
                values = np.nan_to_num(values)
                values = moving_average(values, 7)
                large_fig.append_trace(
                    go.Scatter(x=df.date, y=values, line=dict(color=colors[a]), mode='lines', name=c, legendgroup=c,
                               showlegend=(r == 1)), row=r, col=1)

            a += 1

        r += 1
    large_fig['layout'].update(height=1500, title='Google Mobility Reports (avg 7 days)')
    large_fig.update_layout(template="plotly_white")
    return large_fig





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

countries = ['BE', 'FR', 'NL', 'DE', 'LU', 'GB', 'PT', 'SP', 'IT', 'SE', 'PL']

df = pd.read_csv(f'static/csv/google_mobility_report_eu.csv', parse_dates=['date'])

dfmap = {c: df[df['country_region_code'] == c] for c in countries}

graphs = ['workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline',
          'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
          'parks_percent_change_from_baseline', 'parks_percent_change_from_baseline',
          'transit_stations_percent_change_from_baseline', ]


@register_plot_for_embedding("mobility_plot_eu")
def mobility_plot_eu():
    large_fig = make_subplots(rows=len(graphs), cols=1, subplot_titles=graphs, horizontal_spacing=0.05,
                              vertical_spacing=0.1, shared_yaxes=True)
    r = 1
    for g in graphs:

        fig = go.Figure()

        for c in countries:
            df = dfmap[c]
            large_fig.append_trace(go.Scatter(x=df.date, y=df[g], mode='lines', name=c), row=r, col=1)

        r += 1
    return large_fig
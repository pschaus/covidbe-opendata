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

countries =  ['Belgium','Germany','Netherlands','France','UK','Spain','Italy','Sweden']

df = pd.read_csv(f'static/csv/applemobilitytrends.csv')

cdf = df[df["geo_type"] == "country/region"]

def df_country(country):
    cdf_c = cdf[cdf['region'] == country]
    cdf_c.drop(['geo_type','region'], axis = 1,inplace=True)
    cdf_c.rename(columns={'transportation_type': 'date'},inplace=True)
    cdf_c.set_index(['date'])
    cdf_c=cdf_c.T
    cdf_c.index.name = 'date'
    cdf_c.columns = cdf_c.iloc[0]
    cdf_c.drop(cdf_c.index[0],inplace=True)
    return cdf_c

#{'Australia', 'Philippines', 'South Africa', 'Macao', 'Germany', 'Russia', 'Brazil', 'Romania', 'Slovenia', 'Lithuania', 'Turkey', 'Greece', 'Uruguay', 'Vietnam', 'Croatia', 'Argentina', 'Belgium', 'Netherlands', 'Thailand', 'Iceland', 'Cambodia', 'Slovakia', 'UK', 'Singapore', 'Portugal', 'Ireland', 'Switzerland', 'Israel', 'United Arab Emirates', 'Republic of Korea', 'Ukraine', 'Finland', 'Bulgaria', 'Luxembourg', 'Albania', 'Estonia', 'Indonesia', 'Egypt', 'Saudi Arabia', 'India', 'Italy', 'Serbia', 'Spain', 'United States', 'Austria', 'Czech Republic', 'Morocco', 'Hungary', 'Hong Kong', 'Sweden', 'Japan', 'Chile', 'Poland', 'Latvia', 'Taiwan', 'Malaysia', 'Denmark', 'New Zealand', 'Norway', 'Canada', 'Mexico', 'France', 'Colombia'}
#countries = set(cdf['region'].to_list())

countries_df = {c:df_country(c) for c in countries}

@register_plot_for_embedding("apple_mobility_plot_eu")
def apple_mobility_plot_eu():
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

    graphs = ['driving', 'transit', 'walking', ]
    large_fig = make_subplots(rows=len(graphs), cols=1, subplot_titles=graphs, horizontal_spacing=0.05,
                              vertical_spacing=0.02, shared_xaxes=True)
    r = 1
    for g in graphs:

        fig = go.Figure()
        a = 0
        for c in countries:
            df = countries_df[c]
            large_fig.append_trace(
                go.Scatter(x=df.index, y=df[g], line=dict(color=colors[a]), mode='lines', name=c, legendgroup=c,
                           showlegend=(r == 1)), row=r, col=1)
            a += 1

        r += 1

    large_fig['layout'].update(height=1000, title='Apple Mobility Reports')
    return large_fig





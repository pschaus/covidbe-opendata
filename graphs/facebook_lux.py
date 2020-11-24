import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_babel import get_locale, gettext

from graphs.facebook import population_proportion, population_evolution, movement, staying_put, map_staying_put, \
    map_ratio_tiles_fb
from pages.sources import display_source_providers, source_facebook
from pages import get_translation, display_graphic

import pandas as pd
import plotly.express as px
from graphs import register_plot_for_embedding
import plotly.graph_objs as go


@register_plot_for_embedding("facebook-imported-cases")
def facebook_imported_cases():


    df_fb = pd.read_csv('static/csv/facebook/movement_countries.csv')
    countries = sorted(df_fb.end_name.unique())
    df_fb.rename(columns={'ds': 'date'}, inplace=True)

    df_owid = pd.read_csv('static/csv/owid.csv')
    df_owid['location'] = df_owid['location'].str.lower()

    countries = sorted(df_owid.location.unique())

    df_owid = df_owid[['date', 'location', 'new_cases_smoothed_per_million', 'continent', 'population']]

    df = pd.merge(df_fb, df_owid, how='left', left_on=['date', 'start_name'], right_on=['date', 'location']).drop(
        columns=['location', 'population'])
    df.rename(columns={'new_cases_smoothed_per_million': 'start_new_cases_smoothed_per_million'}, inplace=True)

    df = pd.merge(df, df_owid, how='left', left_on=['date', 'end_name', 'continent'],
                  right_on=['date', 'location', 'continent']).drop(columns=['location'])
    df.rename(columns={'new_cases_smoothed_per_million': 'end_new_cases_smoothed_per_million',
                       'population': 'end_population'}, inplace=True)

    df = df[df.continent == 'Europe']

    df['covid_in'] = 7 * df['start_new_cases_smoothed_per_million'] * df['travel_counts'] / 1000000

    df = df.groupby(['date', 'end_name', 'end_population'])['covid_in'].sum().reset_index()

    df['covid_in_per_million'] = 1000000 * df['covid_in'] / df['end_population']

    df = df[df['end_name'].isin(['austria', 'belgium', 'croatia', 'czech republic', 'denmark'
                                                                                    'estonia', 'finland', 'france',
                                 'germany', 'greece', 'iceland', 'ireland',
                                 'italy', 'lithuania', 'luxembourg', 'netherlands', 'norway'
                                                                                    'romania', 'serbia', 'spain',
                                 'sweden', 'switzerland',
                                 'united kingdom', 'portugal', 'slovenia', 'hungary', 'poland',
                                 'bosnia and herzegovina', 'slovakia', 'bulgaria',
                                 'albania'])]

    countries = df.end_name.unique()

    plots = []
    for c in countries:
        dfc = df[df.end_name == c]
        plot = go.Scatter(x=dfc['date'], y=dfc['covid_in_per_million'].rolling(7).mean(), name=c)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    fig.update_layout(
        height=600,
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="imported cases per million inhabitants", en="imported cases per million inhabitants"))
    )
    return fig


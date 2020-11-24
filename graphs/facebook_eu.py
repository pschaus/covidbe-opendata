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

df_fb = pd.read_csv('static/csv/facebook/movement_countries.csv')
countries = sorted(df_fb.end_name.unique())
df_fb.rename(columns={'ds': 'date'}, inplace=True)

df_owid = pd.read_csv('static/csv/owid.csv')
df_owid['location'] = df_owid['location'].str.lower()

countries = sorted(df_owid.location.unique())

df_owid = df_owid[
    ['date', 'location', 'new_cases_smoothed_per_million', 'continent', 'population', 'new_cases_smoothed']]
df = pd.merge(df_fb, df_owid, how='left', left_on=['date', 'start_name'], right_on=['date', 'location']).drop(
    columns=['location', 'population', 'new_cases_smoothed'])
df.rename(columns={'new_cases_smoothed_per_million': 'start_new_cases_smoothed_per_million'}, inplace=True)
df = pd.merge(df, df_owid, how='left', left_on=['date', 'end_name', 'continent'],
              right_on=['date', 'location', 'continent']).drop(columns=['location'])
df.rename(
    columns={'new_cases_smoothed_per_million': 'end_new_cases_smoothed_per_million', 'population': 'end_population',
             'new_cases_smoothed': 'end_new_cases_smoothed'}, inplace=True)

df = df[df.continent == 'Europe']
df['covid_in'] = 7 * df['start_new_cases_smoothed_per_million'] * df['travel_counts'] / 1000000
df_tot_travel = df.groupby(['date']).agg({'travel_counts': 'sum'}).reset_index()
df = df.groupby(['date', 'end_name', 'end_population', 'end_new_cases_smoothed']).agg(
    {'covid_in': 'sum', 'travel_counts': 'sum'}).reset_index()
df['covid_in_per_million'] = 1000000 * df['covid_in'] / df['end_population']
df['in_per_million'] = 1000000 * df['travel_counts'] / df['end_population']
df['fraction_imported_over_tot_cases'] = df['covid_in'] / df['end_new_cases_smoothed']

df = df[df['end_name'].isin(['austria', 'belgium', 'croatia', 'czech republic', 'denmark'                                                                                'estonia', 'finland', 'france',
                             'germany', 'greece', 'iceland', 'ireland',
                             'italy', 'lithuania', 'luxembourg', 'netherlands', 'norway'                                                                     'romania', 'serbia', 'spain', 'sweden',
                             'switzerland',
                             'united kingdom', 'portugal', 'slovenia', 'hungary', 'poland',
                             'bosnia and herzegovina', 'slovakia', 'bulgaria',
                             'albania'])]

countries = df.end_name.unique()


@register_plot_for_embedding("plot_tot_travel")
def plot_tot_travel():
    fig = px.line(x=df_tot_travel.date.values, y=df_tot_travel.travel_counts.rolling(7).mean())

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    fig.update_layout(
        height=600,
        title="Number of FB users who moved between two EU countries in a 24 hour period (avg 7 days)",
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="Total Flow", en="Total Flow"))
    )
    return fig


@register_plot_for_embedding("plot_tot_fraction_countries")
def plot_tot_fraction_countries():
    traces = []
    for c in countries:
        dfc = df[df.end_name == c]
        trace = dict(x=dfc['date'], y=dfc['travel_counts'].rolling(7).mean(), mode='lines',
                     line=dict(width=0.5),
                     stackgroup='one', groupnorm='percent', name=c)
        traces.append(trace)

    layout = go.Layout(
        showlegend=True,
        yaxis=dict(
            type='linear',
            range=[1, 100],
            dtick=20,
            ticksuffix='%'
        )
    )

    fig = go.Figure(data=traces, layout=layout)


    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    # Edit the layout
    fig.update_layout(title='Fraction of total flow with this destination country',
                      xaxis_title='Date',
                      yaxis_title='Percentage',
                      height=600,)

    return fig


@register_plot_for_embedding("plot_in_per_million")
def plot_in_per_million():
    plots = []
    for c in countries:
        dfc = df[df.end_name == c]
        plot = go.Scatter(x=dfc['date'], y=dfc['in_per_million'].rolling(7).mean(), name=c)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    fig.update_layout(
        height=600,
        title="Daily Incoming users per million inhabitants",
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="Daily Incoming users per million inhabitants",
                            en="Daily Incoming users per million inhabitants"))
    )
    return fig


@register_plot_for_embedding("plot_imported_cases_per_millions")
def plot_imported_cases_per_millions():
    plots = []
    for c in countries:
        dfc = df[df.end_name == c]
        plot = go.Scatter(x=dfc['date'], y=dfc['covid_in_per_million'].rolling(7).mean(), name=c)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    fig.update_layout(
        height=600,
        title="Imported cases per million inhabitants in destination",
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="imported cases per million inhabitants in destination",
                            en="imported cases per million inhabitants in destination"))
    )
    return fig


@register_plot_for_embedding("fraction_imported_cases_over_tot_cases")
def fraction_imported_cases_over_tot_cases():
    plots = []
    for c in countries:
        dfc = df[df.end_name == c]
        plot = go.Scatter(x=dfc['date'], y=dfc['fraction_imported_over_tot_cases'].rolling(7).mean(), name=c)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

    fig.update_layout(
        height=600,
        title="Fraction imported over totcases",
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="fraction_imported_over_tot_cases", en="fraction_imported_over_tot_cases"))
    )
    return fig
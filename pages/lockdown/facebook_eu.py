
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_babel import get_locale, gettext

from pages.sources import display_source_providers, source_facebook
from pages import get_translation, display_graphic
import plotly.graph_objs as go
from graphs.facebook_eu import plot_tot_travel, plot_tot_cases, plot_imported_cases_per_millions,\
    plot_tot_fraction_countries,fraction_imported_cases_over_tot_cases,plot_in_per_million

import pandas as pd
import plotly.express as px


df_all_countries = pd.read_csv('static/csv/facebook/movement_countries.csv')
countries = sorted(df_all_countries.end_name.unique())

def display_facebook_eu():
    return [
        html.H3(
            get_translation(fr="Graphs based on the number of FB users who moved between two EU countries in a 24 hour period (avg 7 days)",
                            en="Graphs based on the number of FB users who moved between two EU countries in a 24 hour period (avg 7 days)")),

        html.Label([gettext(get_translation(fr="Destination Country", en="Destination Country")), dcc.Dropdown(
            id='countries-dropdown-eu',
            options=[{'label': c, 'value': c} for c in countries],
            value='belgium',
            clearable=False
        )],
        style=dict(width='50%')),
        html.Label([gettext(get_translation(fr="Jour", en="Day")), dcc.Dropdown(
            id='countries-day-dropdown-eu',
            options=[{'label': 'all-days-moving-avg-7', 'value': 9},
                     {'label': 'all-days', 'value': 8},
                     {'label': 'monday', 'value': 0},
                     {'label': 'tuesday', 'value': 1},
                     {'label': 'wednesday', 'value': 2},
                     {'label': 'thursday', 'value': 3},
                     {'label': 'friday', 'value': 4},
                     {'label': 'saturday', 'value': 5},
                     {'label': 'sunday', 'value': 6}],
            value=8,
            clearable=False
        )],
        style=dict(width='50%')),
        dcc.Graph(id='graph-countries-eu'),

        dbc.Row([
            dbc.Col(display_graphic(id='plot_tot_travel',
                                    figure=plot_tot_travel(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='plot_tot_travel',
                                    figure=plot_tot_cases(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='plot_tot_fraction_countries',
                                    figure=plot_tot_fraction_countries(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='plot_in_per_million',
                                    figure=plot_in_per_million(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='plot_imported_cases_per_millions',
                                    figure=plot_imported_cases_per_millions(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='fraction_imported_cases_over_tot_cases',
                                    figure=fraction_imported_cases_over_tot_cases(),
                                    config=dict(locale=str(get_locale())))),
        ]),
    display_source_providers(source_facebook)
    ]

def callback_fb_countries_eu(app):
    @app.callback(
        Output('graph-countries-eu', 'figure'),
        [Input('countries-dropdown-eu', 'value'),
         Input('countries-day-dropdown-eu', 'value')])
    def update_graph(country, day):
        df = df_all_countries.loc[df_all_countries.end_name == country]

        df1 = pd.DataFrame({'start_name': df.start_name.unique()})
        df2 = pd.DataFrame({'end_name': df.end_name.unique()})

        df1['travel_counts'] = 0
        df2['travel_counts'] = 0

        df_combinations = df1.merge(df2, how='outer')

        df = pd.concat([df, df_combinations])
        df = df.groupby(['ds', 'start_name', 'end_name']).agg({'travel_counts': 'sum'}).reset_index()

        df.ds = pd.to_datetime(df.ds)
        df.index = df['ds']
        df['day_of_week'] = df.index.dayofweek

        if (day <= 6):
            df = df[df['day_of_week'] == day]

        countries = df.start_name.unique()
        plots = []
        for c in countries:
            dfc = df[df.start_name == c]
            if (day == 9):
                plot = go.Scatter(x=dfc['ds'], y=dfc['travel_counts'].rolling(7).mean(), name=c)
            else:
                plot = go.Scatter(x=dfc['ds'], y=dfc['travel_counts'], name=c)
            plots.append(plot)
        fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

        return fig



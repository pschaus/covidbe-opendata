import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_babel import get_locale, gettext

from graphs.facebook import population_proportion, population_evolution, movement, staying_put, map_staying_put,map_ratio_tiles_fb
from pages.sources import display_source_providers, source_facebook
from pages import get_translation, display_graphic
import plotly.graph_objs as go

import pandas as pd
import plotly.express as px

df_all = pd.read_csv('static/csv/facebook/movement-lux.csv')
regions = sorted(df_all.end_name.unique())

def display_facebook_lux():
    return [
        html.H3(gettext(
            get_translation(
                fr="Flux d'utilisateurs entre arrondissements",
                en="Flux of users between administrative units"))),
        html.P(gettext(
            get_translation(
                fr="""
                Pour chaque arrondissement, on observe l'évolution du flux d'utilisateurs entrant.
                """,
                en="""
                We display for each administrative unit the evolution of incoming users by administrative unit.
                """))),
        html.Label([gettext(get_translation(fr="Arrondissement", en="Administrative unit")), dcc.Dropdown(
            id='region-dropdown-lux',
            options=[{'label': region, 'value':region} for region in regions],
            value='Luxembourg',
            clearable=False
        )],
        style=dict(width='50%')),
        html.Label([gettext(get_translation(fr="Heures de la journée (UTC)", en="Time frame (UTC)")), dcc.Dropdown(
            id='interval-dropdown-lux',
            options=[{'label': '20-4h', 'value':'0000'},
                     {'label': '4-12h', 'value':'0800'},
                     {'label': '12-20h', 'value':'1600'}],
            value='0000',
            clearable=False
        )],
        style=dict(width='50%')),
        dcc.Graph(id='graph-lux'),
        display_source_providers(source_facebook)
        ]

def callback_fb_lux(app):
    @app.callback(
        Output('graph-lux', 'figure'),
        [Input('region-dropdown-lux', 'value'),
         Input('interval-dropdown-lux', 'value')])
    def update_graph(region, interval):
        df = df_all.loc[df_all.end_name == region]
        df = df.loc[df.date_time.str.contains(interval)]

        df1 = pd.DataFrame({'start_name':df.start_name.unique()})
        df2 = pd.DataFrame({'end_name':df.end_name.unique()})
        df3 = pd.DataFrame({'date_time':df.date_time.unique()})

        df1['n_crisis'] = 0
        df2['n_crisis'] = 0
        df3['n_crisis'] = 0

        df_combinations = df1.merge(df2, how='outer').merge(df3, how='outer')

        df = pd.concat([df,df_combinations])
        df = df.groupby(['date_time','start_name','end_name']).agg({'n_crisis':'sum'}).reset_index()

        df.date_time = pd.to_datetime(df.date_time)
        if df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[0],
                y=[0],
                mode="lines+markers+text",
                text=["No Data"],
                textfont_size=40,
            ))
        else:
            fig = px.area(x=df.date_time, y=df.n_crisis, color=df.start_name)

        fig.update_layout(title=gettext(get_translation(fr='Utilisateurs entrant à ', en='Incoming users in '))+region,
                          xaxis_title="date",
                          yaxis_title=gettext(get_translation(fr="nombre d'utilisateurs",en="number of users")),
                          legend_title_text=gettext(get_translation(fr="Venant de", en="Coming from")))

        fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))

        return fig

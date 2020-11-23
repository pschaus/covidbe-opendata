import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_babel import get_locale, gettext
import plotly.graph_objs as go

from graphs.facebook import population_proportion, population_evolution, movement, staying_put, map_staying_put,map_ratio_tiles_fb
from pages.sources import display_source_providers, source_facebook
from pages import get_translation, display_graphic

import pandas as pd
import plotly.express as px

df_all = pd.read_csv('static/csv/facebook/movement.csv')
regions = sorted(df_all.end_name.unique())

def display_facebook():
    return [
        html.P(gettext(
            get_translation(
                fr="""
                Toutes les données présentées dans les visualisations ci-dessous concernent uniquement les utilisateurs de Facebook ayant activé leur localisation.
                """,
                en="""
                All data visualized below only concerns Facebook users who activate their localization.
                """))),
        html.H3(gettext(
            get_translation(
                fr="Changement du nombre de tuiles visitées quotidiennement par rapport à la normale",
                en="Change in the daily number of tiles visited wrt normality"))),
        html.Span(gettext(
            get_translation(
                fr="Une ",
                en="A "))),
        html.A(gettext(get_translation(fr="tuile", en="tile")), href="https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system", target="_blank"),
        html.Span(gettext(
            get_translation(
                fr="""
                est zone géographique de 600x600m. L'indicateur représenté sur le graphe présente pour chaque jour le changement dans la mobilité des utilisateurs par rapport à la normale.
                Plus précisément, c'est le nombre moyen de tuiles différentes visitées sur une journée divisé par cette valeur en temps normal.
                Les valeurs caractérisant la normalité ont été calculées sur les 45 jours précédant le début du graphe et pour chacun des jours de la semaine.
                """,
                en="""
                is a 600x600m geographical area. The metric shown on the graph indicates the daily evolution of the mobility to a normal period.
                More precisely, it is the average number of unique tiles visited during a day divided by that same value computed for a normal period.
                Values considered as normal were computed over the 45 days before the start of this graph and for each separate weekday.
                """))),
        dbc.Row([
            dbc.Col(display_graphic(id='movement',
                              figure=movement(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='ratio-tiles-map',
                                    figure=map_ratio_tiles_fb(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext(
            get_translation(
                fr="Fraction des utilisateurs restant dans la même tuile toute la journée (moyenne 7 jours)",
                en="Ratio of users staying in one tile for the whole day (avg 7 days)"))),
        html.Span(gettext(
            get_translation(
                fr="Comme pour le graphe précédent, on considère des zones géographiques de 600x600m (",
                en="As for the previous graph, we consider 600x600m geographical areas ("))),
        html.A(gettext(get_translation(fr="tuiles", en="tiles")), href="https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system", target="_blank"),
        html.Span(gettext(
            get_translation(
                fr=""").
                Cet indicateur donne une idée de la proportion de la population restant à (ou très proche de) son domicile toute la journée.
                Par exemple, si je rends visite à mes grand-parents qui habitent le village voisin à quelques kilomètres de chez moi,
                je vais traverser plusieurs tuiles sur la journée et ainsi faire partie des utilisateurs n'étant pas restés fixes pendant toute la journée.
                """,
                en=""").
                This metric gives insights about the fraction of the population who stays at home (or close to it) during the whole day.
                For instance, if I visit my grandparents in a village distant by a few kilometers, I will cross several tiles and thus
                will not belong to the users who stayed put for the whole day.
                """))),
        dbc.Row([
            dbc.Col(display_graphic(id='staying-put',
                              figure=staying_put(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='staying-put-map',
                                    figure=map_staying_put(),
                                    config=dict(locale=str(get_locale())))),
        ]),
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
            id='region-dropdown',
            options=[{'label': region, 'value':region} for region in regions],
            value='Brussel Hoofdstad',
            clearable=False
        )],
        style=dict(width='50%')),
        html.Label([gettext(get_translation(fr="Heures de la journée (UTC)", en="Time frame (UTC)")), dcc.Dropdown(
            id='interval-dropdown',
            options=[{'label': '20-4h', 'value':'0000'},
                     {'label': '4-12h', 'value':'0800'},
                     {'label': '12-20h', 'value':'1600'}],
            value='0000',
            clearable=False
        )],
        style=dict(width='50%')),
        dcc.Graph(id='graph'),
        html.H3(gettext(
            get_translation(
                fr="Lien de proportionnalité entre le nombre d'utilisateurs et la population réelle",
                en="Proportionality between the number of users and the population"))),
        html.P(gettext(
            get_translation(
                fr="""
                Comparaison du nombre d'utilisateurs de Facebook observés en moyenne chaque jour de la semaine (calculé sur 45 jours avant le 14 avril 2020) et de la population de chaque arrondissement.
                On observe une relation linéaire respectée dans tous les arrondissements.
                Les arrondissements de Soignies et La Louvière ne figurent pas sur cette visualisation car les données fournies par Facebook ne tiennent pas compte de la division de Soignies de janvier 2019.
                """,
                en="""
                Comparison of the average number of Facebook users by weekday (computed over 45 days before April 14th 2020) with the population of each administrative unit.
                We observe a linear relation for all administrative units.
                Soignies and La Louvière are not shown on the visualization as Facebook data does not account for the split of Soignies in January 2019.
                """))),
        dbc.Row([
            dbc.Col(display_graphic(id='population-proportion',
                              figure=population_proportion(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_facebook)
        ]

def callback_fb(app):
    @app.callback(
        Output('graph', 'figure'),
        [Input('region-dropdown', 'value'),
         Input('interval-dropdown', 'value')])
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

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.facebook import population_proportion
from pages.sources import display_source_providers, source_facebook
from pages import get_translation

def display_facebook():
    return [
        html.H3(gettext("Proportionality between the number of users and the population")),
        html.P(gettext(
            get_translation(
                fr="""
                Comparaison du nombre d'utilisateurs de Facebook et de la population de chaque arrondissement.
                On observe une proportionnalité respectée dans tous les arrondissements.
                Les arrondissements de Soignies et La Louvière ne figurent pas sur cette visualisation car les données fournies par Facebook ne tiennent pas compte de la division de Soignies de janvier 2019.
                """,
                en="""
                Comparison of the number of Facebook users with the population of each administrative unit.
                We observe a proportionality for all administrative units.
                Soignies and La Louvière are not shown on the visualization as Facebook data does not account for the split of Soignies in January 2019.
                """))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='population-proportion',
                              figure=population_proportion(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_facebook)
        ]

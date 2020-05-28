import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.brussels import brussels_tunnels, brussels_tunnels_ratio, brussels_alltunnels_ratio, apple_mobility_plot_cities, bike_mobility_plot_stations
from pages.sources import display_source_providers, source_google_traffic, source_brussels_mobility, source_apple_mobility
from pages import get_translation

def display_brussels():
    return [
        html.H3(gettext("Tunnel traffic")),
        html.P(gettext(
            get_translation(
                fr="""Nombre de véhicules passant chaque heure dans les tunnels principaux de Bruxelles.""",
                en="""Number of vehicles passing every hour through the main tunnels of Brussels."""))),
        html.H3(gettext("Brussels tunnels traffic working days 7:00-8:00")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-tunnel',
                              figure=brussels_tunnels(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Brussels tunnels relative traffic working days 7:00-8:00")),
        html.P(gettext(
            get_translation(
                fr="""Divisé par le nombre moyen de véhicules enregistré sur la période 1er Féb - 10 Mars""",
                en="""Divided by the average number of vehicles recorded over the period Feb 1 - March 10"""))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-tunnel-ratio',
                              figure=brussels_tunnels_ratio(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Brussels all tunnels relative traffic working days 7:00-8:00")),
        html.P(gettext(
            get_translation(
                fr="""Divisé par le nombre moyen de véhicules enregistré sur la période 1er Féb - 10 Mars""",
                en="""Divided by the average number of vehicles recorded over the period Feb 1 - March 10"""))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-tunnel-ratio',
                              figure=brussels_alltunnels_ratio(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_brussels_mobility),
        html.H2(gettext("Apple Mobility Report")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='eucities-apple',
                              figure=apple_mobility_plot_cities(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_apple_mobility),
        html.H2(gettext("Brussels Mobility: bike relative passage count through stations")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-bikes-ratio',
                              figure=bike_mobility_plot_stations(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_brussels_mobility),

    ]

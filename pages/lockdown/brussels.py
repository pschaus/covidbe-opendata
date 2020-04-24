import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.brussels import brussels_tunnels, brussels_tunnels_ratio
from pages.sources import display_source_providers, source_google_traffic, source_brussels_mobility
from pages import get_translation

def display_brussels():
    return [
        html.H2(gettext("Brussels tunnels traffic working days 7:00-8:00")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-tunnel',
                              figure=brussels_tunnels(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Brussels tunnels relative traffic working days 7:00-8:00")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='brussels-tunnel-ratio',
                              figure=brussels_tunnels_ratio(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_brussels_mobility),

    ]

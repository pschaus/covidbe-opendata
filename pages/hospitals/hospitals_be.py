import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.hopitals import bar_hospitalization


def display_hospitals():
    return [
        html.H2(gettext("Hospitalization")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-be',
                              figure=bar_hospitalization(),
                              config=dict(locale=str(get_locale())))),
        ]),
    ]

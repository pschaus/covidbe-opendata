import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.hopitals import bar_hospi_per_case_per_province
from pages.sources import display_source_providers, source_sciensano


def display_hospitals_prov():
    return [
        html.H2(gettext("Hospitalizations per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=bar_hospi_per_case_per_province(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

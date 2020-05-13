import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.cases_per_admin_region import map_totcases_admin_region, map_cases_per_habittant_admin_region
from pages.sources import *


def display_admin():
    return [
        html.H2(gettext("Total Number of cases since the beginning")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=map_totcases_admin_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Total Number of cases per inhabitant")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=map_cases_per_habittant_admin_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]
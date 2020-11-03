import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext
from pages import AppLink, get_translation, display_graphic

from graphs.cases_region import cases_absolute_region,cases_relative_region
from pages.sources import *


def display_region():
    return [
        html.H2(gettext(
            get_translation(en="Average number of cases on 7 days",
                            fr="Nombre de cas moyen sur 7 jours"))),
        dbc.Row([
            dbc.Col(display_graphic(id='casesregion', figure=cases_absolute_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='casesrelregion', figure=cases_relative_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]
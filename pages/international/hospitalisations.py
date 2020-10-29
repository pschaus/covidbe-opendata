# Inspired from https://covid19dashboards.com/covid-compare-permillion/
# and https://gist.github.com/gschivley/578c344461100071b7eef158efccce95


from pages import get_translation, display_graphic
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext
from graphs.hopitals_international import hospi_international,icu_international

import io

import numpy as np
import altair as alt
#config InlineBackend.figure_format = 'retina'

from graphs.cases_per_million import lines_cases_per_million_not_log
from pages.sources import source_opendataecdc, display_source_providers


def display_hospi_international():

    return [
    html.H1(get_translation(
            en="""Hospitalizations per 100K""",
            fr="""Hospitationsation par 100K""",)),
    dbc.Row([
                   dbc.Col(display_graphic(id='hospi_international', figure=hospi_international(),
                                     config=dict(locale=str(get_locale()))), className="col-12"),
    ]),
    dbc.Row([
                   dbc.Col(display_graphic(id='icu_international', figure=icu_international(),
                                     config=dict(locale=str(get_locale()))), className="col-12"),
    ]),
        display_source_providers(source_opendataecdc)
    ]

def callback_display_hospi_international(app):
    return None
# Inspired from https://covid19dashboards.com/covid-compare-permillion/
# and https://gist.github.com/gschivley/578c344461100071b7eef158efccce95


from pages import get_translation, display_graphic
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext


import io

import numpy as np
import altair as alt
#config InlineBackend.figure_format = 'retina'

from graphs.cases_per_million import lines_cases_per_million_not_log
from pages.sources import source_hopkins, display_source_providers


def display_cases_per_million():

    return [
    html.H1(get_translation(
            en="""Cases per million""",
            fr="""Cas par million""",)),
    dcc.Markdown(get_translation(
            en="""
                The number of reported cases per million is a lower bound on the actual number of infected persons per million inhabitants. Countries have had different testing capabilities and approaches.
                """,
            fr="""
            Le nombre de cas signalés par million est une limite inférieure du nombre réel de personnes infectées par million d'habitants. Les pays ont eu différentes capacités et approches pour réaliser les tests de dépistage.
            """,
        )),
    dbc.Row([
                   dbc.Col(display_graphic(id='cases per country', figure=lines_cases_per_million_not_log(),
                                     config=dict(locale=str(get_locale()))), className="col-12"),
    ]),
        display_source_providers(source_hopkins)
    ]

def callback_cases_per_million(app):
    return None


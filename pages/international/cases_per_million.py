# Inspired from https://covid19dashboards.com/covid-compare-permillion/
# and https://gist.github.com/gschivley/578c344461100071b7eef158efccce95

import dash_core_components as dcc
import dash_html_components as html
from pages import get_translation

import io

import numpy as np
import altair as alt
#config InlineBackend.figure_format = 'retina'

from graphs.cases_per_million import lines_cases_per_million
from pages.sources import source_hopkins, display_source_providers


def display_cases_per_million():

    plot1=lines_cases_per_million()
    # Save html as a StringIO object in memory
    plot1_html = io.StringIO()
    plot1.save(plot1_html, 'html')

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
    html.Iframe(
        id='plot',
        height='500',
        width='1000',
        sandbox='allow-scripts',

        # This is where we pass the html
        srcDoc=plot1_html.getvalue(),

        # Get rid of the border box
        style={'border-width': '0px'}
    ),
        display_source_providers(source_hopkins)
    ]

def callback_cases_per_million(app):
    return None


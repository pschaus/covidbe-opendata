# Inspired from https://covid19dashboards.com/covid-compare-permillion/
# and https://gist.github.com/gschivley/578c344461100071b7eef158efccce95

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from os.path import isfile
from app import app
from pages import get_translation

import io

import numpy as np
import altair as alt
#config InlineBackend.figure_format = 'retina'

from graphs.deaths_per_million import lines_deaths_per_million



def display_deaths_per_million():

    plot1=lines_deaths_per_million()
    # Save html as a StringIO object in memory
    plot1_html = io.StringIO()
    plot1.save(plot1_html, 'html')

    return [
    html.H1(get_translation(
            en="""Deaths per million""",
            fr="""Morts par million""",)),
    dcc.Markdown(get_translation(
            en="""
                The number of reported deaths per million is a lower bound on the actual number of deaths per million inhabitants. Some countries have likely not reported all cases.
                """,
            fr="""
            Le nombre de décès signalés par million est une limite inférieure du nombre réel de décès par million d'habitants. Certains pays n'ont probablement pas signalé tous les cas.
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
    )
    ]

def callback_deaths_per_million(app):
    return None


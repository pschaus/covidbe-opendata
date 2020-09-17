import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.hopitals import bar_hospitalization, hospi_over_death_smooth,hospi_smooth,death_smooth
from pages.sources import display_source_providers, source_sciensano


def display_hospitals():
    return [
        html.H2(gettext("Hospitalization")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-be',
                              figure=bar_hospitalization(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total Hospitalization Avg over 7 past days")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-be',
                              figure=hospi_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total Deaths Avg over 7 past days")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-be',
                              figure=death_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total Deaths/ Total Hospitalization (Avg over 7 past days)")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-be',
                              figure=hospi_over_death_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),

        display_source_providers(source_sciensano)
    ]

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from graphs.vaccines_be import plot_vaccines_cumulated
from pages import display_graphic
from pages.sources import source_sciensano, source_statbel, display_source_providers

from pages import get_translation, display_graphic

def display_vaccines():
    return [
        html.H2(gettext("Vaccines")),
        dcc.Markdown(get_translation(
            fr="""Vaccins COVID Belgiques""",
            en="""Covid Vaccines Belgium""")),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines',
                              figure=plot_vaccines_cumulated(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano),
    ]

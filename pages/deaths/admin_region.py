import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext


from graphs.deaths_be_statbel import death_arrondissements_map_weekly
from pages.sources import source_sciensano, source_statbel, display_source_providers

from pages import get_translation

def display_arrondissements():
    return [
        html.H3(get_translation(en="Weekly Mortality In each admin region (STATBEL Data)",fr="Mortalité par semaine dans chaque arrondissement (STATBEL Data)")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='death-statbel-weekly-adminregion',
                              figure=death_arrondissements_map_weekly(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_statbel),
    ]

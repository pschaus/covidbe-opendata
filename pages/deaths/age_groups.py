import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from pages.sources import source_sciensano, display_source_providers


def display_age_groups():
    return [
        html.H2(gettext("Age groups")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-death',
                              figure=age_groups_death(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-death-pie',
                              figure=age_groups_death_pie(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

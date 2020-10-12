import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from graphs.deaths_be_statbel import death_age_groups
from graphs.deaths_be_statbel_hist import death_85plus_hist,death_85plus_hist_cum,death_plus_hist_cum,death_hist
from pages.sources import source_sciensano, source_statbel, display_source_providers


def display_covid_death():
    return [
        html.H2(gettext("COVID (Daily) Mortality (Sciensano Data)")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-death-stack',
                              figure=age_groups_death("stack"),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-death-pie',
                              figure=age_groups_death_pie(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

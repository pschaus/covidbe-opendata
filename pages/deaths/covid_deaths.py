import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie, \
    waves_comparison,region_death_covid,region_covid_death_per_habitant
from pages import display_graphic
from pages.sources import source_sciensano, source_statbel, display_source_providers
from graphs.hopitals import death_smooth

def display_covid_death():
    return [
        html.H2(gettext("COVID (Daily) Mortality (Sciensano Data)")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-stack',
                              figure=age_groups_death(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='region_death_covid',
                                    figure=region_death_covid(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='region_death_covid_per_habitant',
                                    figure=region_covid_death_per_habitant(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total Deaths Avg over 7 days")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be',
                              figure=death_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("First wave vs 2nd wave")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be-waves',
                              figure=waves_comparison(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Since March")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-pie',
                              figure=age_groups_death_pie(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

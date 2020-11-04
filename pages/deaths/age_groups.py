import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from graphs.deaths_be_statbel import death_age_groups
from graphs.deaths_be_statbel_hist import death_plus_hist_cum, \
    daily_death_all, daily_death_ag, daily_death_all_deviation_sin,death_cum_january,death_cum_january_additional
from pages import display_graphic
from pages.sources import source_sciensano, source_statbel, display_source_providers


def display_age_groups():
    return [
        html.H2(gettext("Overall (Daily) Mortality All Population (STATBEL Data)")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-statbel-sinplot',
                              figure=daily_death_all(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-statbel-sinplot-deviation',
                              figure=daily_death_all_deviation_sin(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Overall (Daily) Mortality By Age-group (STATBEL Data)")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-statbel-daily',
                              figure=daily_death_ag(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Overall (Weekly) Mortality Only (STATBEL Data)")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-statbel-weekly',
                              figure=death_age_groups("stack"),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-death-statbel-stack',
                              figure=death_age_groups(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("History of death all population")),
        dbc.Row([
             dbc.Col(display_graphic(id='death-statbell-all-hist-cum',
                               figure=death_plus_hist_cum(),
                               config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='death_cum_january',
                                    figure=death_cum_january(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='death_cum_january_additional',
                                    figure=death_cum_january_additional(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_statbel),
    ]

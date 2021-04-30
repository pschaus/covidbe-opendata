import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from graphs.vaccines_be import plot_vaccines_cumulated, vaccine_nis5, fig_ag_dose_a_c
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
        html.H2(get_translation(
            fr="""Percentage of 1st dose (A or C) in each region per age-group""",
            en="""Percentage of 1st dose (A or C) in each region per age-group""")),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-age-group-region',
                                    figure=fig_ag_dose_a_c(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2(get_translation(
            fr="""Percentage of 1st dose (A or C) in each municipality per age-group""",
            en="""Percentage of 1st dose (A or C) in each municipality per age-group""")),

        html.H2("85+"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-85+',
                                    figure=vaccine_nis5('85+'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2("75-84"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-75-84',
                                    figure=vaccine_nis5('75-84'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2("65-74"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-65-74',
                                    figure=vaccine_nis5('65-74'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2("55-64"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-55-64',
                                    figure=vaccine_nis5('55-64'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2("45-54"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-45-54',
                                    figure=vaccine_nis5('45-54'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2("35-44"),
        dbc.Row([
            dbc.Col(display_graphic(id='vaccines-35-44',
                                    figure=vaccine_nis5('35-44'),
                                    config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano),
    ]

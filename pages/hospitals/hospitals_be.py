import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.hopitals import bar_hospitalization, \
    hospi_over_death_smooth,\
    hospi_smooth,death_smooth,\
    icu_over_hospi,newin_smooth,\
    death_over_icu_smooth, \
    bar_hospitalization_ICU, \
    bar_hospitalization_tot, \
    bar_hospitalization_in_out,\
    bar_hospitalization_in,\
    exp_fit_hospi,hospi_waves, gees_barometer, average_age_new_in
from pages import display_graphic
from pages.sources import display_source_providers, source_sciensano


def display_hospitals():
    return [
        html.H2(gettext("Total Hospitalizations")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be-tot',
                              figure=bar_hospitalization_tot(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total ICU Hospitalizations")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be-icu',
                                    figure=bar_hospitalization_ICU(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Daily IN-OUT Hospitalizations")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be-in',
                                    figure=bar_hospitalization_in(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-be-in-out',
                                    figure=bar_hospitalization_in_out(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("GEES Barometer")),
        dbc.Row([
            dbc.Col(display_graphic(id='gees barometer',
                                    figure=gees_barometer(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total ICU/ Total Hospitalization")),
        dbc.Row([
            dbc.Col(display_graphic(id='icuoverhospi',
                              figure=icu_over_hospi(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Deaths/ Total ICU (Avg over 7 past days)")),
        dbc.Row([
            dbc.Col(display_graphic(id='deathovericu',
                              figure=death_over_icu_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Deaths/ Total Hospitalization (Avg over 7 past days)")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospioverdeath',
                              figure=hospi_over_death_smooth(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Average age weekly admission")),
        dbc.Row([
            dbc.Col(display_graphic(id='avg age weekly admission',
                                    figure=average_age_new_in(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

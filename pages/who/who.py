import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.deaths_age_groups import age_groups_death, age_groups_death_pie
from graphs.who_indicators import death_oms, posrate_oms, newin_oms, cases_oms
from pages import display_graphic
from pages.sources import source_sciensano, source_statbel, display_source_providers

from pages import get_translation, display_graphic

def display_who():
    return [
        html.H2(gettext("New Hospitalization WHO Indicator")),
        dcc.Markdown(get_translation(
            fr="""Taux d’hospitalisation = Nombre de nouvelles hospitalisations dues à la COVID-19 pour 100 000 habitants et par semaine (moyenne sur deux semaines).""",
            en="""Hospitalization rate = Number of new hospitalizations due to COVID-19 per 100,000 inhabitants per week (average over two weeks).""")),
        dbc.Row([
            dbc.Col(display_graphic(id='newinoms',
                              figure=newin_oms(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Positive Rate WHO Indicator")),
        dcc.Markdown(get_translation(
            fr="""Taux de positivité = Proportion de tests positifs (moyenne sur deux semaines)""",
            en="""Positivity rate = Proportion of positive tests (average over two weeks)""")),
        dbc.Row([
            dbc.Col(display_graphic(id='posrate_oms',
                              figure=posrate_oms(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Cases Incidence WHO Indicator")),
        dcc.Markdown(get_translation(
            fr="""Incidence des cas = Nombre de cas confirmés pour 100 000 habitants et par semaine (moyenne sur deux semaines). """,
            en="""Incidence = number of confirmed cases per 100 000 inhabitants per week (averaged over two weeks). """)),
        dbc.Row([
            dbc.Col(display_graphic(id='cases_oms',
                                figure=cases_oms(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("COVID Death WHO Indicator")),
        dcc.Markdown(get_translation(
            fr="""Mortalité = Nombre de décès attribués à la COVID-19 pour 100 000 habitants et par semaine (moyenne sur deux semaines)""",
            en="""Mortality = Number of deaths attributed to COVID-19 per 100,000 population per week (two-week average) """)),
        dbc.Row([
            dbc.Col(display_graphic(id='death_oms',
                                    figure=death_oms(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano),
    ]

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.cases_per_admin_region import map_totcases_admin_region, map_cases_per_habittant_admin_region
from graphs.cases_per_admin_region_overtime import map_totcases_admin_region_overtime, \
    map_cases_per_habittant_admin_region_overtime,\
    plot_cases_admin_region_overtime,\
    plot_cases_per_habittant_admin_region_overtime, \
    plot_cases_daily_admin_region_overtime,\
    map_cases_incidence_nis3,\
    scatter_incidence_nis3
from pages.sources import *

from pages import get_translation, display_graphic


def display_admin():
    return [
        html.H2(gettext(
            get_translation(en="Number of cases per admin region", fr="Nombre de cas par arrondissement"))),
        html.P(gettext(
            get_translation(
                fr="""C'est le nombre de cas testés positifs rapportés par Sciensano. 
                      Le nombre de cas positifs réel peut être (beaucoup) plus important.
                      Notez que le nombre de tests quotidien augmente également. Voir notre page testing.
                """,
                en="""
                This is the number of positive test cases reported by Sciensano. 
                The number of actual positive cases can be (much) higher.
                Note that the number of daily tests is also increasing. See our testing page."""))),

        html.H3(gettext(
            get_translation(en="Incidence: Number of cases/100K inhabitants over the past 14 days", fr="Incidence: Nombre de cas/100K habitants sur les 14 derniers jours"))),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-province-map', figure=map_cases_incidence_nis3(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-province-scatter-incidence', figure=scatter_incidence_nis3(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H3(gettext(
            get_translation(en="Plot over time  (double click in the legend to isolate one region)", fr="Evolution dans le temps (double click dans la legende pour isoler une region)"))),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-province-daily-bar-chart', figure=plot_cases_daily_admin_region_overtime(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-province-daily-bar-chart-perhabittant', figure=plot_cases_per_habittant_admin_region_overtime(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H3(gettext(get_translation(en="Total Number of cases since beginning", fr="Nombre de cas total depuis le début"))),
        dbc.Row([
            dbc.Col(display_graphic(id='tot-cases-province-map', figure=map_totcases_admin_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H3(gettext(get_translation(en="Total Number of cases per 1000 inhabitants since the beginning",
                                        fr="Nombre de cas total pour 1000 habitants depuis le début "))),
        dbc.Row([
            dbc.Col(display_graphic(id='perhabittant-cases-province-map', figure=map_cases_per_habittant_admin_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]
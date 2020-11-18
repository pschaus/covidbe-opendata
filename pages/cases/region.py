import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext
from pages import AppLink, get_translation, display_graphic

from graphs.cases_region import cases_relative_region,positive_rate_region,\
    number_of_test_per_inhabitant_region,ratio_case_hospi_region
from pages.sources import *


def display_region():
    return [
        html.H2(gettext(
            get_translation(en="Positive cases (avg 7 days)",
                            fr="Numbre de cas positifs (moy 7 jours)"))),
        dbc.Row([
            dbc.Col(display_graphic(id='casesrelregion', figure=cases_relative_region(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext(
            get_translation(en="Positive Rate % (avg 7 days)",
                            fr="Taux de positivité % (moy 7 jours)"))),
        dbc.Row([
            dbc.Col(display_graphic(id='positive_rate_region', figure=positive_rate_region(),
                                    config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext(
            get_translation(en="Number of tests/ 100K inhabitants (avg 7 days)",
                            fr="Nombre de tests/ 100K habitant (moy 7 jours)"))),
        dbc.Row([
            dbc.Col(display_graphic(id='number_of_test_per_inhabitant_region', figure=number_of_test_per_inhabitant_region(),
                                    config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext(
            get_translation(en="Ratio New Hospi (avg 7 days) / Cases (avg 7 days)",
                            fr="Ratio New Hospi (moy 7 jours) / Cas (moy 7 jours)"))),
        dbc.Row([
            dbc.Col(display_graphic(id='ratio_case_hospi_region',
                                    figure=ratio_case_hospi_region(),
                                    config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano, source_map_provinces)
    ]
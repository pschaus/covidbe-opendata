import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.testing import bart_plot_cases_testing, plot_ration_cases_over_testing, \
    plot_cumulated_testing, plot_ration_cases_over_testing_smooth,test_vs_case_increase
from pages import display_graphic
from pages.sources import display_source_providers, source_sciensano


def display_testing():
    return [
        html.H2(gettext("Number of cases and tests each day")),
        dbc.Row([
            dbc.Col(display_graphic(id='testing-barplot', figure=bart_plot_cases_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Ratio #Cases/#Tests averaged over past 7 days")),
        dbc.Row([
            dbc.Col(display_graphic(id='cases-over-testing', figure=plot_ration_cases_over_testing_smooth(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Case vs Test increase")),
        dbc.Row([
            dbc.Col(display_graphic(id='test_vs_case_increase', figure=test_vs_case_increase(),
                                    config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Cumulated #Tests and #Cases")),
        dbc.Row([
            dbc.Col(display_graphic(id='cumulated-testing', figure=plot_cumulated_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano)
    ]
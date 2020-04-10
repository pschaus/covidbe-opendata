import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.testing import bart_plot_cases_testing, plot_ration_cases_over_testing, plot_cumulated_testing

def display_testing():
    return [
        html.H2("Number of cases and tests each day"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=bart_plot_cases_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2("Ratio #Cases/#Tests each day"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=plot_ration_cases_over_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2("Cumulated #Tests and #Cases"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=plot_cumulated_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ])


    ]
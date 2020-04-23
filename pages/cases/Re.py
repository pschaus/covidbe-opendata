import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.Re import plot_ration_cases_over_testing
from pages.sources import display_source_providers, source_sciensano


def display_Re():
    return [
        html.H2(gettext("Effective number of secondary infections (Re factor)")),
        html.P("As we only have access to the cases tested positive at time t (without knowing exactly when they are not active anymore), we have to make some hypotheses to estimate the Re."), 
        dcc.Markdown('''
        * If we consider that it takes n days for an active patient to recover, 
        * If we make a moving average over 7 days of the positive patients, 
        '''), 
        html.P("Then here are the curves that we obtain since the lockdown in Belgium:"), 
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=plot_ration_cases_over_testing(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_sciensano)
    ]
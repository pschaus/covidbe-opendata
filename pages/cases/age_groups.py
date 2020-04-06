import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from graphs.cases_age_groups import  fig_age_groups_cases


def display_age_groups():
    return [
        html.H2("Age groups"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases', figure=fig_age_groups_cases), ),
        ]),

    ]

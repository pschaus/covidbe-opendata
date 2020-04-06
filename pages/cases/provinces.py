import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from graphs.cases_per_province import map_provinces, barplot_provinces_cases

def display_provinces():
    return [
        html.H2("Number of cases / 1000 inhabitants"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cases-province-map', figure=map_provinces), ),
            dbc.Col(dcc.Graph(id='cases-province-barplot', figure=barplot_provinces_cases), ),

        ])
    ]
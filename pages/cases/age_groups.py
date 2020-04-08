import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.cases_age_groups import age_groups_cases, age_groups_cases_pie


def display_age_groups():
    return [
        html.H2(gettext("Age groups")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases',
                              figure=age_groups_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases-pie',
                              figure=age_groups_cases_pie(),
                              config=dict(locale=str(get_locale())))),
        ])
    ]

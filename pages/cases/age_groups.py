import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.cases_age_groups import age_groups_cases, age_groups_cases_pie, age_groups_pop_active_cases, age_groups_pop_active_hypothetical
from pages.sources import display_source_providers, source_sciensano
from pages import get_translation




def display_age_groups():
    return [
        html.H2(get_translation(fr = "Nombre de case par groupe d'age",en="Number of cases per age group")),
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
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases',
                              figure=age_groups_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases',
                              figure=age_groups_pop_active_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),

        html.P(gettext(
            get_translation(
                fr="""Hypothetical""",
                en="""Hypothetical"""))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases',
                              figure=age_groups_pop_active_hypothetical(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='age-group-cases-pie',
                              figure=age_groups_cases_pie(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

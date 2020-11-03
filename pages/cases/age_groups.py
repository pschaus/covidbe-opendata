import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.cases_age_groups import age_groups_cases, age_groups_cases_pie, age_groups_pop_active_cases, \
    age_groups_pop_active_hypothetical, average_age_cases, age_group_cases_relative, incidence_age_group_plot
from pages.sources import display_source_providers, source_sciensano
from pages import get_translation, display_graphic


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
            dbc.Col(display_graphic(id='age-group-cases',
                              figure=age_groups_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-cases-distribution-percentage',
                              figure=age_group_cases_relative(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(get_translation(fr = "Nombre de cas par 100K dans la population du groupe d'age",en="Number of cases per 100K in the age group population")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-cases-relative100K',
                              figure=incidence_age_group_plot(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(get_translation(fr="Nombre de cas dans chaque groupe d'age",
                                en="Nombre de cas dans chaque groupe d'age")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-cases-60years',
                              figure=age_groups_pop_active_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(get_translation(fr="Evolution de l'age moyen des cas",
                                en="Evolution of the average age of cases")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-cases-average-agge',
                              figure=average_age_cases(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(get_translation(fr="Repartition de cas depuis le début de l'épidémie",
                                en="Distribution of cases since the beginning")),
        dbc.Row([
            dbc.Col(display_graphic(id='age-group-cases-pie',
                              figure=age_groups_cases_pie(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

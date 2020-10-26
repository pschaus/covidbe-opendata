import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext


from graphs.deaths_be_statbel import death_arrondissements_map_weekly
from graphs.cases_death_per_admin_region_overtime import gapminder_case_death_admin_region_overtime
from pages.sources import source_sciensano, source_statbel, display_source_providers

from pages import get_translation, display_graphic


def display_arrondissements():
    return [
        html.H3(get_translation(en="Weekly Mortality In each admin region (STATBEL Data)",fr="Mortalité par semaine dans chaque arrondissement (STATBEL Data)")),
        dbc.Row([
            dbc.Col(display_graphic(id='death-statbel-weekly-adminregion',
                              figure=death_arrondissements_map_weekly(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_statbel),

        html.H3(get_translation(en="Weekly Mortality vs Number of case In each admin region per 1000 inhabitants",
                                fr="Mortalité vs Nombre de case par semaine dans chaque arrondissement pour 1000 habitants")),

        html.P(gettext(
            get_translation(
                fr="""La surface des cercles represente la population des arrondissements.""",
                en="""The circcle surface represents the population of the region."""))),
        dbc.Row([
            dbc.Col(display_graphic(id='gapminder-adminregion',
                              figure=gapminder_case_death_admin_region_overtime(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_statbel),
        display_source_providers(source_sciensano),
    ]

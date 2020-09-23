import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext
from graphs.hopitals_prov import total_hospi_new_in_provinces,\
    total_hospi_new_out_provinces,\
    total_hospi_provinces,total_icu_provinces,\
    map_hospi_provinces,map_hospi_per100K_provinces,\
    scatter_hospi_provinces,\
    scatter_hospi_per100K_provinces
from graphs.hopitals import bar_hospi_per_case_per_province
from pages.sources import display_source_providers, source_sciensano


def display_hospitals_prov():
    return [
        html.H2(gettext("Total hospitalizations per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov-map',
                              figure=map_hospi_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov-scatter',
                              figure=scatter_hospi_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization100K-prov-map',
                              figure=map_hospi_per100K_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization100K-prov-scatter',
                              figure=scatter_hospi_per100K_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=total_hospi_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total ICU per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=total_icu_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total daily new hospitalizations per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=total_hospi_new_in_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total daily persons out of hospital per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=total_hospi_new_out_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Hospitalizations per province")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hospitalization-prov',
                              figure=bar_hospi_per_case_per_province(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

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
    scatter_hospi_per100K_provinces, \
    hospi_new_in_per_provinces, hospi_provinces_per100k, new_in_per_100K_provinces
from graphs.hopitals import bar_hospi_per_case_per_province
from pages import display_graphic
from pages.sources import display_source_providers, source_sciensano


def display_hospitals_prov():
    return [
        html.H3(gettext("New Hospitalization per province")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-prov-w1w2',
                              figure=hospi_new_in_per_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='in-out-prov',
                                    figure=total_hospi_new_in_provinces(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='in_per100k_prov',
                                    figure=new_in_per_100K_provinces(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Total number of hospitalizations per province")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization-prov-total',
                              figure=total_hospi_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Total number of hospitalizations per province per 100K inhabitants")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospi_provinces_per100k',
                                    figure=hospi_provinces_per100k(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Total number of hospitalizations Per 100K inhabitants")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization100K-prov-map',
                              figure=map_hospi_per100K_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='hospitalization100K-prov-scatter',
                              figure=scatter_hospi_per100K_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Total ICU per province")),
        dbc.Row([
            dbc.Col(display_graphic(id='icu-prov',
                              figure=total_icu_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H3(gettext("Total daily persons out of hospital per province")),
        dbc.Row([
            dbc.Col(display_graphic(id='newout-prov',
                              figure=total_hospi_new_out_provinces(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

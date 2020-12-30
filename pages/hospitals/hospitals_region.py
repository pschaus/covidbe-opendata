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
    hospi_w1w2_provinces, hospi_provinces_per100k
from graphs.hopitals import bar_hospi_per_case_per_province
from graphs.hopitals_region import hospi_total_in_region_per100k, \
    hospi_total_in_icu_region_per100k, hospi_newin_region_per100k, hospi_newout_region_per100k
from pages import display_graphic
from pages.sources import display_source_providers, source_sciensano


def display_hospitals_region():
    return [
        html.H2(gettext("Total hospitalizations per region")),
        html.H3(gettext("Total number of hospitalizations per region per 100K inhabitants")),
        dbc.Row([
            dbc.Col(display_graphic(id='hospi_total_in_region_per100k',
                                    figure=hospi_total_in_region_per100k(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='hospi_total_in_icu_per100k',
                                    figure=hospi_total_in_icu_region_per100k(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='hospi_newin_region_per100k',
                                    figure=hospi_newin_region_per100k(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='hospi_newout_region_per100k',
                                    figure=hospi_newout_region_per100k(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_sciensano)
    ]

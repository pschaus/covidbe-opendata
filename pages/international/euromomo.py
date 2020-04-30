import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.euromomo import euromomo_zscores
from pages import custom_warning_box
from pages.sources import display_source_providers, source_euromomo


def display_euromomo():
    return [
        html.H2(gettext("EUROMOMO data analysis")),
        html.H3(gettext("Where are the peaks?")),
        custom_warning_box(gettext("Z-scores CANNOT be compared country-to-country. The plot below can only be used to"
                                   " find when the peaks happened.")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='euromomo-zscores',
                              figure=euromomo_zscores(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_euromomo)
    ]

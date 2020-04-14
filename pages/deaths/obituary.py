import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.obituary import inmemoriam_plot, sudpresse_plot, dansnospensees_plot, allbeobituary_plot, avideces_plot, rolling_ratio_plot, bar_plot_be, bar_plot_fr
from pages.sources import *


def display_obituary():
    return [
        html.H2(gettext("Evolution of the number of deaths published on obituary websites 2020 vs 2019")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='inmemoriam',
                              figure=inmemoriam_plot(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),
            dbc.Col(dcc.Graph(id='sudpress',
                              figure=sudpresse_plot(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),
            dbc.Col(dcc.Graph(id='dansnospensees',
                              figure=dansnospensees_plot(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),
            dbc.Col(dcc.Graph(id='allbeobituary',
                              figure=allbeobituary_plot(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),
            dbc.Col(dcc.Graph(id='avisdeces',
                              figure=avideces_plot(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),

        ]),
        html.H2(gettext("Ratio of number of deaths published on obituary websites 2020/2019")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='rollinrationobituary',
                              figure=rolling_ratio_plot(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Total number of deaths published on obituary websites 2020/2019")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='allbeobituarybar',
                              figure=bar_plot_be(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6),
            dbc.Col(dcc.Graph(id='allfrobituarybar',
                              figure=bar_plot_fr(),
                              config=dict(locale=str(get_locale()))),
                    width=12, lg=6)
        ]),



        display_source_providers(source_inmemoriam, source_necro_sudpress)
    ]

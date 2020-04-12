import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.obituary import inmemoriam_plot, sudpresse_plot


def display_obituary():
    return [
        html.H2(gettext("Evolution of the number of deaths published on obituary websites")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='inmemoriam',
                              figure=inmemoriam_plot(),
                              config=dict(locale=str(get_locale())))),
            dbc.Col(dcc.Graph(id='sudpress',
                              figure=sudpresse_plot(),
                              config=dict(locale=str(get_locale())))),
        ]),
    ]

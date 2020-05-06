import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.tomtom_traffic import plot_tomtom_be_working_days
from pages.sources import display_source_providers, source_tomtom
from pages import get_translation

def display_tomtom():
    return [
        html.H2(gettext("TomTom Traffic")),
        dcc.Markdown(get_translation(
            en="""
    The TomTom traffic index is the additional time needed as compared to a 30-minutes trip in uncongested conditions.
    A 53% congestion level in Brussels, for example, means that a 30-minute trip will take 53% more time than it would during Brussels’s baseline uncongested conditions.
    It thus means that you will need 45.9 minutes total average travel time instead of 30 minutes (in uncongested conditions).

    We record this data daily to measure the release of the lockdown constraints.
        """,
            fr="""
    L'indice de trafic TomTom est le temps supplémentaire nécessaire par rapport à un trajet de 30 minutes dans des conditions non encombrées.
    Un niveau de congestion de 53% à Bruxelles, par exemple, signifie qu’un voyage de 30 minutes prendra 53% de temps de plus qu’un trajet sans encombrement à Bruxelles.
    Cela signifie donc que vous aurez besoin d'un temps de trajet moyen total de 45,9 minutes au lieu de 30 minutes (dans des conditions non encombrées).

    Nous enregistrons ces données quotidiennement depuis le 14 avril pour mesurer le déconfinement.
            """, )),
        html.H2(gettext("TomTom Traffic Index Belgium Cities 07:00-9:00")),
        dbc.Row([
            dbc.Col(dcc.Graph(id='google map usage',
                              figure=plot_tomtom_be_working_days(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_tomtom),
    ]

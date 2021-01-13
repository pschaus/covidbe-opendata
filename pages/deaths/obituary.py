import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.obituary import dans_nos_pensees,sud_presse
from pages.sources import *
from pages import get_translation, display_graphic


def display_obituary():
    return [

        html.H2(gettext("Evolution of the number of deaths published on obituary websites")),
        dcc.Markdown(get_translation(
            fr="""
            Les données rapportées sont téléchargées des sites mortuaires belges (necro.sudpress.be, dansnospensees.be). 
            Au total, nous capturons environ 1/3 des décès en Belgique. 
            Nous pensons que cela est suffisamment représentatif de la situation de surmortalité due au COVID19. 
            La Flandre et Bruxelles semblent sous représentés dans les sites belges et reflète dès lors davantage la situation en Wallonie.
            """,
            en="""
            The reported data are crawled from the Belgian (necro.sudpress.be, dansnospensees.be) mortuary sites daily.
            In total, we capture around 1/3 of the daily deaths in Belgium with these data.
            We believe that this is sufficiently representative of the excess mortality situation due to COVID19.
            Flanders and Brussels seem underrepresented in Belgian sites and therefore more closely reflect the situation in Wallonia.
            """, )),
        dbc.Row([
            dbc.Col(display_graphic(id='sud_presse',
                                    figure=sud_presse(),
                                    config=dict(locale=str(get_locale())))),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='dans_nos_pensees',
                              figure=dans_nos_pensees(),
                              config=dict(locale=str(get_locale())))),
        ]),

        display_source_providers(source_inmemoriam, source_necro_sudpress)
    ]

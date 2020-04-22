import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.obituary import inmemoriam_plot, sudpresse_plot, dansnospensees_plot, allbeobituary_plot, avideces_plot, rolling_ratio_plot, bar_plot_be, bar_plot_fr, ratio_plot
from pages.sources import *
from pages import get_translation

def display_obituary():
    return [

        html.H2(gettext("Evolution of the number of deaths published on obituary websites 2020 vs 2019")),
        dcc.Markdown(get_translation(
            fr="""
            Les données rapportées sont téléchargées des sites mortuaires belges (inmemoriam.be, necro.sudpress.be, dansnospensees.be) et français (avisdeces.fr) quotidiennement. 
            Au total, nous capturons environ 1/3 des décès en Belgique et en France avec ces données. 
            Nous pensons que cela est suffisamment représentatif de la situation de surmortalité due au COVID19. 
            La Flandre et Bruxelles semblent sous représentés dans les sites belges et reflète dès lors davantage la situation en Wallonie.
            """,
            en="""
            The reported data are crawled from the Belgian (inmemoriam.be, necro.sudpress.be, dansnospensees.be) and French (avisdeces.fr) mortuary sites daily.
            In total, we capture around 1/3 of the daily deaths in Belgium and France with these data.
            We believe that this is sufficiently representative of the excess mortality situation due to COVID19.
            Flanders and Brussels seem underrepresented in Belgian sites and therefore more closely reflect the situation in Wallonia.
            """, )),
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
        dcc.Markdown(get_translation(
            fr="""
        Ce graphique montre la surmortalité instantanée en Belgique et en France par rapport à 2019.
        Un ratio de 2 signifie que nous avons 2x plus de morts qu'en 2019 et un ratio de 1 signie le même nombre de morts.
        Afin de réduire l'effet due au fluctuation journalière, ce ratio est calculé sur une fenêtre (glissante) de 7 jours.
        """,
            en="""
        This graph shows the instant excess mortality in Belgium and France compared to 2019.
        A ratio of 2 means that we have 2x more deaths than in 2019 and a ratio of 1 means the same number of deaths.
        In order to reduce the effect due to the daily fluctuation, this ratio is calculated on a (sliding) window of 7 days.
            """, )),
        dbc.Row([
            dbc.Col(dcc.Graph(id='rollinratio_obituary',
                              figure=rolling_ratio_plot(),
                              config=dict(locale=str(get_locale())))),
        ]),
        html.H2(gettext("Ratio of number of deaths published on obituary websites 2020/ average 2019")),
        dcc.Markdown(get_translation(
            fr="""
            Même graphique que le précédent, mais le ratio est calculé par rapport à la moyenne 2019 pour éviter d'ajouter des fluctuations dues à 2019.
            """,
            en="""
            Same graph as the previous one, but the ratio is calculated relative to the 2019 average to avoid adding fluctuations due to 2019.
            """, )),
        dbc.Row([
            dbc.Col(dcc.Graph(id='ratio_obituary',
                              figure=ratio_plot(),
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

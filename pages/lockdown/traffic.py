import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.google_traffic import plot_google_traffic_working_days
from pages.sources import display_source_providers, source_google_traffic
from pages import get_translation, display_graphic


def display_traffic():
    return [
        html.H2(gettext("Google Map Usage working days 8:00-8:30")),
        dcc.Markdown(get_translation(
            fr="""
Google enregistre le ratio entre le taux de demande (trafic) dans cette région et le taux de demande au niveau mondial pour chacune des applications.
Nous pensons que l'application google map est intéressante à observer, car elle reflète l'impact du confinement.
Afin de comparer les pays, nous normalisons la courbe d'un pays par rapport à la moyenne des 10 premiers jours de mars.
Une valeur de 1 signifie que la proportion du trafic de ce pays et la même que les 10 premiers jours de mars.
Une valeur inférieure à 1 signifie que le pays a perdu des parts de trafic par rapport aux 10 premiers jours de mars.
La mobilité dans ce pays semble comparativement plus réduite que la normale relativement aux autres pays.
Une valeur supérieure à 1 signifie que le pays a gagné du trafic par rapport aux 10 premiers jours de mars.
La mobilité dans ce pays semble comparativement supérieure à la normale relativement aux autres pays.
    """,
            en="""
Google records the ratio between the demand rate (traffic) in this region and the global demand rate for each of the applications.
We think the google map app is interesting to study because it reflects the impact of the lockdown.
In order to compare the countries, we normalize the curve of a country compared to the average of the first 10 days of March.
A value of 1 means that the proportion of traffic from this country is the same as the first 10 days of March.
A value less than 1 means that the country has lost traffic shares compared to the first 10 days of March.
Mobility in this country seems comparatively lower than normal compared to other countries.
A value greater than 1 means that the country has gained traffic compared to the first 10 days of March.
Mobility in this country seems comparatively higher than normal compared to other countries.
        """, )),
        dbc.Row([
            dbc.Col(display_graphic(id='google map usage',
                              figure=plot_google_traffic_working_days(),
                              config=dict(locale=str(get_locale())))),
        ]),
        display_source_providers(source_google_traffic),
    ]

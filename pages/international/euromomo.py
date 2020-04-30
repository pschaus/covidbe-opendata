import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from flask_babel import get_locale, gettext

from graphs.euromomo import euromomo_zscores, euromomo_ratio
from pages import custom_warning_box
from pages.sources import display_source_providers, source_euromomo
from pages import get_translation


def display_euromomo():
    return [
        html.H2(gettext("EUROMOMO data analysis")),
        html.H3(gettext("Overmortality Comparison")),
        dcc.Markdown(get_translation(
            fr="""
    EuroMOMO donne les courbes des z-score chaque semaine.
    Le problème est qu'un z-score ne permet pas une comparaison aisée relative entre les pays. 
    Il permet plutôt d'attirer l'attention sur une anomalie par rapport à la normale, mais il ne permet en aucun cas d'estimer l'excès de mortalité d'un pays à l'autre sur une même semaine.
    
    La formule d'un z-score est (x(t)-baseline) / sd. Il est tout à fait raisonnable de considérer que la baseline et l'écart type (sd) sont constant depuis la pandémie du COVID19.
    Si nous connaissons la mortalité hebdomadaire d'un pays pour deux semaines différentes, nous pouvons donc résoudre un système de deux équations à deux inconnues pour retrouver les valeurs baseline et sd propres à chaque pays.
    Voici les valeurs que nous avons retrouvées pour certains pays.
     

    | Country      | baseline | sd |
    |--------------|----------|--------------------|
    | UK (England) | 10954    | 154                |
    | Netherlands  | 3024     | 84                 |
    | Belgium      | 2166     | 68                 |
    | France       | 10391    | 251                |

    Nous avons tracés ci dessous la courbe x(t) ainsi retrouvée divisée par la baseline.
    Cette courbe nous donne une bonne estimation de la surmortalité chaque semaine dans les pays.
    """,
            en="""
    EuroMOMO gives the z-score curves every week.
    The problem is that a z-score does not allow an easy relative comparison between countries.
    Rather, it draws attention to an abnormality compared to normal, but it does not in any case allow to estimate the excess mortality from one country to another over the same week.
    
    The formula for a z-score is (x(t)-baseline) / sd. It is entirely reasonable to consider that the baseline and the standard deviation (sd) have been constant since the COVID19 pandemic.
    If we know the weekly mortality of a country for two different weeks, we can therefore solve a system of two equations with two unknowns to find the baseline and sd values specific to each country.
    Here are the values that we found for certain countries.


    | Country      | baseline | sd |
    |--------------|----------|--------------------|
    | UK (England) | 10954    | 154                |
    | Netherlands  | 3024     | 84                 |
    | Belgium      | 2166     | 68                 |
    | France       | 10391    | 251                |


    We have plotted below the curve x (t) thus found divided by the baseline.
    This curve gives us a good estimate of the excess mortality each week in the countries.
    """, )),

        dbc.Row([
            dbc.Col(dcc.Graph(id='euromomo-ratio',
                              figure=euromomo_ratio(),
                              config=dict(locale=str(get_locale())))),
        ]),
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

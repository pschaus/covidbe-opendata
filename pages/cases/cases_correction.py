import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale

from graphs.cases_age_groups import age_groups_pop_active_hypothetical, age_groups_pop_active_cases
from graphs.overmortality import daily_deaths, daily_deaths_respiratory, overmortality_respiratory_line, \
    overmortality_estimates_repartition, overmortality_respiratory_count
from pages import model_warning, get_translation
from pages.sources import *


def display_cases_correction():
    return [
        dcc.Markdown(get_translation(
            fr="""
                        ## Et si la première vague n'était pas correcte?
                    """,
        )),
        *model_warning(
            dcc.Markdown(get_translation(
                fr="""
                    Nous entendons souvent que la deuxième vague est fort différente de la première, car celle-ci touche 
                    beaucoup plus les jeunes (c’est-à-dire la population active <60 ans, en bleu ci-dessus) que lors de 
                    la première vague qui touchait essentiellement les >60 ans (en rouge). 
                    C’est en effet ce que montrent les données brutes.
                """,
            )),
            dbc.Row([
                dbc.Col(dcc.Graph(id='age-group-cases',
                                  figure=age_groups_pop_active_cases(),
                                  config=dict(locale=str(get_locale())))),
            ]),
            dcc.Markdown(get_translation(
                fr=""" 
                    Cependant, une phrase de la conférence de presse de Sciensano aujourd’hui peut nous 
                    laisser penser que ceci n’est pas correct et que nous pourrions légitimement redessiner 
                    la première vague afin que celle-ci colle plus avec la réalité. C’est l’exercice que nous faisons ici.
                    
                    Faisons d’abord quelques hypothèses qui nous paraissent réalistes.
                    Supposons tout d'abord qu’une personne positive dans sa tranche d'âge aujourd’hui à la même probabilité 
                    de terminer hospitalisée qu’au début de l’épidémie. 
                    Appelons cette hypothèse la stabilité de la dangerosité du virus 
                    (cette hypothèse pourrait ne pas être vraie si sa virulence s´est affaiblie mais ceci n'a pas été 
                    démontré à l´heure actuelle).
                    
                    Sciensano annonce aujourd’hui durant la conférence de presse que, depuis le 22 juin, 
                    l'âge médian des personnes hospitalisées est de 65 ans, or avant cette date il était plutôt de 70 ans. 
                    Nous pouvons donc supposer que la distribution d’âge des personnes hospitalisées est restée relativement stable 
                    (merci à Sciensano de mettre les données à disposition pour que nous puissions confirmer ou infirmer cette hypothèse). 
                    
                    En utilisant notre hypothèse de stabilité de la dangerosité du virus, 
                    cela signifierait qu’il doit y avoir environ la même proportion de cas positifs dans les tranches d'âge 
                    aujourd’hui que durant la première vague. 
                    
                    Utilisons cette déduction pour tenter de corriger la courbe des contaminations de la première vague.
    
                    Depuis le 22 juin, 14% des tests positifs concernent des personnes de plus de 60 ans. 
                    Le testing est beaucoup plus exhaustif aujourd’hui, nous allons donc supposer que cette proportion est correcte.
    
                    Supposons que le nombre  de personnes de plus de 60 ans contaminées était correct également durant la 
                    première vague. Cette hypothèse est probablement fausse puisque nous testions alors uniquement les cas 
                    symptomatiques, mais elle est cependant conservatrice pour notre exercice de correction de la courbe.
    
                    Cela signifierait que nous pouvons multiplier le nombre de cas de moins de 60 ans par un facteur 
                    correctif 1/14% = 7.14. Nous obtenons alors cette courbe corrigée des cas positifs mettant en 
                    perspective l’importance de la première vague par rapport au rebond que nous connaissons depuis mi-juillet:
                """,
            )),
            dbc.Row([
                dbc.Col(dcc.Graph(id='age-group-cases',
                               figure=age_groups_pop_active_hypothetical(),
                               config=dict(locale=str(get_locale())))),
            ]),
            display_source_providers(source_sciensano,)
        )
    ]
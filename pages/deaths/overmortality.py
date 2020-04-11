import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale

from graphs.overmortality import daily_deaths, daily_deaths_respiratory, overmortality_respiratory_line, \
    overmortality_estimates_repartition, overmortality_respiratory_count
from pages import model_warning, get_translation


def display_overmortality():
    age_estimate, pie_estimate = overmortality_estimates_repartition()

    return [
        dcc.Markdown(get_translation(
            en="""
                ## Overmortality analysis
                
                Many persons have died from Covid-19, but some of them would have died even in the absence of the coronavirus
                in Belgium. The amount of deceased people that are not in this category is called the **overmortality**.
                
                This page attempts at giving ideas and estimates about the overmortality attributable to the Covid-19.
                
                ### 1. Covid-19 daily deaths against *all* expected deaths
                """,
            fr="""
                ## Analyse de la surmortalité

                Beaucoup de personnes sont décédées du Covid-19, mais plusieurs d'entre elles seraient décédées 
                d'autres causes si le coronavirus n'était pas présent en Belgique. Le nombre de personnes qui ne sont
                pas dans ce cas est appelé la **surmortalité** imputable au coronavirus.
                
                Cette page tente de donner une idée et une estimation de la surmortalité due au coronavirus.

                ### 1. Décès journaliers liés au Covid-19 comparés aux décès attendus
            """,
        )),
        dcc.Graph(figure=daily_deaths(), config=dict(locale=str(get_locale()))),
        dcc.Markdown(get_translation(
            en="""
            This graphic plots side-by-side the amount of expected death during an average day in Belgium (in 2018, this
            amounts to approximately 300 deaths each day), and the amount of people that died from Covid-19. The number
            of coronavirus-linked deaths is already significant compared to the expected death count. 
            
            These two numbers cannot be added directly: many people that died from the coronavirus would have died from
            other causes during the year: there is an intersection between the sets.
            
            ### 2. Covid-19 daily deaths against expected deaths *from respiratory diseases*
            
            We can nevertheless estimate this intersection. In Belgium, in 2016, approximately 10% of the deaths were 
            due to a respiratory problem (more or less 30 persons per day). 
            """,
            fr="""
            Ce graphique montre côte-à-côte le nombre de décès attendus pendant un jour moyen en Belgique (en 2018, 
            c'était environ 300 décès par jour), et le nombre de décès liés au Covid-19. On notera que le nombre
            de décès dûs au Covid-19 est déjà élevé par rapport à la mortalité attendue.
            
            Ces deux nombres (mortalité "normale" et mortalité "supplémentaire" due au coronavirus) ne peuvent pas être
            additionnée directement: plusieurs personnes décédée du Covid-19 seraient de toute façon décédée dans un 
            futur proche d'autres causes. Il y a donc une intersection entre ces deux ensembles.
            
            ### 2. Mortalité journalière du Covid-19 comparée à la mortalité attendue *des maladies respiratoires*
            
            Nous pouvons néanmoins estimer cette intersection. En Belgique, en 2016, approximativement 10% des décès 
            étaient imputables à des problèmes respiratoires (environ 30 décès par jour).
            """
        )),
        dcc.Graph(figure=daily_deaths_respiratory(), config=dict(locale=str(get_locale()))),
        dcc.Markdown(get_translation(
            en="""
            As death induced by the coronavirus will be attributed to the respiratory illness category, we can compute
            the overmortality in that particular category (shown in grey in the plot). The overmortality computed this 
            way is thus a **lower bound** on the effective overmortality: some people die from respiratory diseases 
            not linked to the coronavirus, even during this period.
            
            ### 3. Overmortality per day **from respiratory diseases**
            
            We can apply this equation on every day since the beginning of the epidemy:
            """,
            fr="""
            Etant donné que les morts dûes au coronavirus seront attribuées à la catégorie des décès causés par des
            problèmes respiratoires, nous pouvons calculer la surmortalité dans cette catégorie particulière (montrée
            en gris dans le graphique ci-dessus). La surmortalité calculée de cette manière est en fait une 
            sous-estimation de la surmortalité effective (pour cause respiratoire): malgré le coronavirus, des
            personnes continuent de mourir de cause respiratoires non liées au Covid-19.
            
            ### 3. Surmortalité journalière **de cause respiratoire**
            
            Nous pouvons appliquer ce calcul pour chaque jour depuis le début de l'épidémie:
            """
        )),
        dcc.Graph(figure=overmortality_respiratory_line(), config=dict(locale=str(get_locale()))),
        dcc.Markdown(get_translation(
            en="""
            Since the beginning of the epidemy, this amounts to {total} deaths in overmortality in the respiratory 
            diseases category.
            
            ### 4. Estimating general overmortality
            """,
            fr="""
            Depuis le début de l'épidémie, cela représente {total} décès en surmortalité (toujours, et uniquement, 
            dans la catégorie des décès liés à des problèmes respiratoires).
            
            ### 4. Estimer la surmortalité générale
            """
        ).format(total=int(overmortality_respiratory_count()))),
        *model_warning(
            dcc.Markdown(get_translation(
                en="""
                We computed the overmortality due to respiratory illnesses; it does not give us directly information about 
                the overmortality in general. We must take into account these factors:
                - The actual overmortality in the respiratory illness category is actually higher (everyone is not dying 
                  from the Covid-19 in that category);
                - there will be undermortality due to the coronavirus in other categories (car accidents, for example, 
                  occur less due to confinement). Additionally, some people dying from coronavirus infection would have 
                  died from other causes;
                - there will be overmortality in other categories, for example an increase in suicides, and problems due to 
                  people going less often to the doctor and the hospital for other illnesses.
        
                All-in-all, we can make the hypothesis that the respiratory surmotality is a good estimate of the effective 
                overmortality (we actually expect it to be lower than the truth). This overmortality is to be compared with 
                the other sources of mortality. Let us take an example for a specific day:
                """,
                fr="""
                Nous avons calculé ci-dessus la surmortalité dans la catégorie des maladies respiratoires; cela ne nous
                donne pas d'information à propos de la surmortalité générale. Nous devons prendre en compte ces 
                facteurs:
                - The surmortalité réelle dans la catégorie des maladies respiratoires est en vérité plus élevée que le
                  calcul ci-dessus (tout le monde dans cette catégorie ne meurt pas du Covid-19);
                - il y aura une sous-mortalité, causée par le coronavirus, dans d'autres catégorie (par exemple,
                  moins d'accidents de voiture grâce au confinement). Par ailleurs, certaines personnes décédées du
                  coronavirus seraient décédées d'autres causes dans un futur proche;
                - une surmortalité sera présente également dans d'autres catégories: par exemple, l'on peut s'attendre
                  à une augmentation des suicides dûe au confinement, et à des maladies non prises en charge à temps 
                  étant donné que la population évite les hopitaux.
                  
                En prenant tout ces facteurs en compte, l'on peut poser l'**hypothèse** que la surmortalité respiratoire 
                est une estimation raisonable de la surmortalité totale (nous nous attendons à ce qu'elle soit en fait
                une sous-estimation). Cette surmortalité doit être comparée par rapport aux autres facteurs de décès.
                On peut prendre l'exemple d'un jour moyen:
                """
            )),
            dcc.Graph(figure=age_estimate, config=dict(locale=str(get_locale()))),
            dcc.Graph(figure=pie_estimate, config=dict(locale=str(get_locale())))
        )
    ]
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import gettext, get_locale

from graphs.overmortality import daily_deaths, daily_deaths_respiratory, overmortality_respiratory_line, \
    overmortality_estimates_repartition
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
        dcc.Markdown(gettext("""
            This graphic plots side-by-side the amount of expected death during an average day in Belgium (in 2018, this
            amounts to approximately 300 deaths each day), and the amount of people that died from Covid-19. The number
            of coronavirus-linked deaths is already significant compared to the expected death count. 
            
            These two numbers cannot be added directly: many people that died from the coronavirus would have died from
            other causes during the year: there is an intersection between the sets.
            
            ### 2. Covid-19 daily deaths against expected deaths *from respiratory diseases*
            
            We can nevertheless estimate this intersection. In Belgium, in 2016, approximately 10% of the deaths were 
            due to a respiratory problem (more or less 30 persons per day). 
            """)),
        dcc.Graph(figure=daily_deaths_respiratory(), config=dict(locale=str(get_locale()))),
        dcc.Markdown(gettext("""
            As death induced by the coronavirus will be attributed to the respiratory illness category, we can compute
            the overmortality in that particular category (shown in grey in the plot). The overmortality computed this 
            way is thus a **lower bound** on the effective overmortality: some people die from respiratory diseases 
            not linked to the coronavirus, even during this period.
            
            ### 3. Overmortality per day **from respiratory diseases**
            
            We can apply this equation on every day since the beginning of the epidemy:
            """)),
        dcc.Graph(figure=overmortality_respiratory_line(), config=dict(locale=str(get_locale()))),
        dcc.Markdown(gettext("""
            Since the beginning of the epidemy, this amounts to {total} deaths in overmortality in the respiratory 
            diseases category.""")),

        dcc.Markdown(gettext("""### 4. Estimating general overmortality""")),
        *model_warning(
            dcc.Markdown(gettext("""
                We computed the overmortality due to respiratory illnesses; it does not give us directly information about 
                the overmortality in general. Let us make some hypotheses:
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
            """)),
            dcc.Graph(figure=age_estimate, config=dict(locale=str(get_locale()))),
            dcc.Graph(figure=pie_estimate, config=dict(locale=str(get_locale())))
        )
    ]
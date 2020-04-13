import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_babel import get_locale, gettext, lazy_gettext

from pages import AppMenu, AppLink, get_translation


def display_index():
    return [
        dbc.Jumbotron([
            html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            html.Div([
                dcc.Markdown(get_translation(
            en="""
                                We gather data about the Coronavirus in Belgium, and attempt to extract meaningful information from it.
    
                                 Each menu on the left (or above the page if you are on a phone) shows a different analysis.
                                 
                                 
                                 Most of our visualization are interactive, use your mouse and fingers to play with it.
                                 """,
            fr="""
                                Nous collectons des données sur le Coronavirus en Belgique et tentons d'en extraire des informations significatives.

                                 Chaque menu à gauche (ou au-dessus de la page si vous êtes sur un smartphone) montre une analyse différente.

                                 La plupart de nos visualisations sont interactives, utilisez votre souris et vos doigts pour interagir avec.""",))
            ], className="index_first")
        ]),
        html.H3(["Open Data"]),
        dcc.Markdown(get_translation(
            en="""
                We use open and/or public data to enable these analyses. Our sources are indicated below each analysis.
                
                
                All the source code [Github repository](https://github.com/pschaus/covidbe-opendata), graphics and data
                we produce are available under the [OPEN COVID LICENSE 1.0](https://opencovidpledge.org/license/v1-0/).
                In short, feel free to use them without any restriction.
                    
            """,
            fr="""
                Nous utilisons des données ouvertes et/ou publiques pour permettre ces analyses. Nos sources sont indiquées sous chaque analyse.
                
                
                Tout le code source [référentiel Github] (https://github.com/pschaus/covidbe-opendata), graphiques et données
                que nous produisons sont disponibles sous [OPEN COVID LICENSE 1.0] (https://opencovidpledge.org/license/v1-0/).
                En résumé, vous pouvez les utiliser sans aucune restriction.
                    
            """,)),
        html.H3([get_translation(
                en="Contributing to the project",
                fr="Contribuer au projet",
                )]),
        dcc.Markdown(get_translation(
            en="""
                Whether you are a doctor, epidemiologist,  a data analysis specialist, or a member of the general public, you 
                may have
                - questions that we may be able to answer with more data, 
                - some data that we could use (and open to the public!),
                - ideas of new analysis that we could do.
                
                We are also working on a survey project to collect data to prepare the lift of the lockdown. If you are a doctor or epidemiologist and want
                to help us in the design of this survey, please contact us. 

                You can reach us by email (see the [About page](/about)) or twitter [@Covidatabe](https://twitter.com/Covidatabe).
                We gladly accept new contributions as pull-requests [Github repository](https://github.com/pschaus/covidbe-opendata) !
            """,
            fr="""
                Que vous soyez médecin, épidémiologiste, spécialiste de l'analyse des données ou membre du grand public, vous
                pouvez avoir
                - des questions auxquelles nous pourrons peut-être répondre avec plus de données,
                - des données que nous pourrions utiliser (et les rendre disponible au public!),
                - des idées de nouvelles analyses que nous pourrions faire.
                
                Nous travaillons également sur un projet d'enquête pour collecter des données afin de préparer la levée du confinement. Si vous êtes médecin ou épidémiologiste et que vous souhaitez
                nous aider dans la conception de cette enquête, merci de nous contacter.

                Vous pouvez nous joindre par e-mail (voir la [page À propos] (/about)) ou twitter [@Covidatabe] (https://twitter.com/Covidatabe).
                Nous acceptons volontiers les nouvelles contributions via pull-requests [dépôt Github] (https://github.com/pschaus/covidbe-opendata)!
            """,))
    ]


def display_about():
    return [html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            dcc.Markdown(get_translation(
            en="""
            We are a team specialized in [AI, Analytics](https://aia.info.ucl.ac.be/people/) and [Computer Science](https://uclouvain.be/fr/instituts-recherche/icteam/ingi) from @UCLouvain_be and @EPL_ECLouvain.
            We produce this website with the hope it can help you to better understand and objectively analyze the impact of the COVID crisis on Belgium and his sub-regions.
            
            The current main contributors to this project are:
 
            - [Guillaume Derval, UCLouvain](https://www.linkedin.com/in/guillaumederval/)
            - [Pierre Schaus, UCLouvain](https://www.info.ucl.ac.be/~pschaus)
            - [Vincent François, UCLouvain](http://vincent.francois-l.be)
            
            """,
            fr="""
            Nous sommes une équipe spécialisée en [AI, Analytics] (https://aia.info.ucl.ac.be/people/) et [Informatique] (https://uclouvain.be/fr/instituts-recherche/icteam / ingi) de @UCLouvain_be et @EPL_ECLouvain.
            Nous produisons ce site Internet dans l'espoir qu'il puisse vous aider à mieux comprendre et analyser objectivement l'impact de la crise COVID sur la Belgique et ses régions.

            Les principaux contributeurs actuels de ce projet sont:
 
            - [Guillaume Derval, UCLouvain] (https://www.linkedin.com/in/guillaumederval/)
            - [Pierre Schaus, UCLouvain] (https://www.info.ucl.ac.be/~pschaus)
            - [Vincent François, UCLouvain] (http://vincent.francois-l.be)

            """,))
    ]





index_menu = AppMenu('index', '', [
    AppLink(lazy_gettext("Home"), lazy_gettext("Home"), '/index', display_index),
    AppLink(lazy_gettext("About"), lazy_gettext("About"), '/about', display_about)
], fake_menu=True)

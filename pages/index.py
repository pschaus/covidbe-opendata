import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_babel import get_locale, gettext

from pages import AppMenu, AppLink, get_translation


def display_index():
    return [
        dbc.Jumbotron([
            html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            html.Div([
                dcc.Markdown("""
                                 We gather data about the Coronavirus in Belgium, and attempt to extract meaningful information from it.
    
                                 Each menu on the left (or above the page if you are on a phone) shows a different analysis.
                                 
                                 
                                 Most of our visualization are interactive, use your mouse and fingers to play with it.
                                 """)
            ], className="index_first")
        ]),
        html.H3(["Open Data"]),
        dcc.Markdown("""
                We use open and/or public data to enable these analyses. Our sources are indicated below each analysis.
                
                
                All the source code [Github repository](https://github.com/pschaus/covidbe-opendata), graphics and data
                we produce are available under the [OPEN COVID LICENSE 1.0](https://opencovidpledge.org/license/v1-0/).
                In short, feel free to use them without any restriction.
                
            """),
        html.H3(["Contributing to the project"]),
        dcc.Markdown("""
                Whether you are a doctor, epidemiologist,  a data analysis specialist, or a member of the general public, you 
                may have
                - questions that we may be able to answer with more data, 
                - some data that we could use (and open to the public!),
                - ideas of new analysis that we could do.
                
                We are also working on a survey project to collect data to prepare the lift of the lockdown. If you are a doctor or epidemiologist and want
                to help us in the design of this survey, please contact us. 

                You can reach us by email (see the [About page](/about)) or twitter [@Covidatabe](https://twitter.com/Covidatabe).
                We gladly accept new contributions as pull-requests [Github repository](https://github.com/pschaus/covidbe-opendata) !
            """)
    ]


def display_about():
    return [html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            dcc.Markdown("""
            We are a team specialized in [AI, Analytics](https://aia.info.ucl.ac.be/people/) and [Computer Science](https://uclouvain.be/fr/instituts-recherche/icteam/ingi) from @UCLouvain_be and @EPL_ECLouvain.
            We produce this website with the hope it can help you to better understand and objectively analyze the impact of the COVID crisis on Belgium and his sub-regions.
            
            The current main contributors to this project are:
 
            - [Guillaume Derval, UCLouvain](https://www.linkedin.com/in/guillaumederval/)
            - [Pierre Schaus, UCLouvain](https://www.info.ucl.ac.be/~pschaus)
            - [Vincent François, UCLouvain](http://vincent.francois-l.be)
            
            """)
    ]





index_menu = AppMenu('index', '', [
    AppLink("Home", "Home", '/index', display_index),
    AppLink("About", "About", '/about', display_about)
], fake_menu=True)

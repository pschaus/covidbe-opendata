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
    
                                 Each menu on the left (or above the page if you are on a phone) shows a different analysis.""")
            ], className="index_first")
        ]),
        html.H3(["Open Data"]),
        dcc.Markdown("""
                We use open and/or public data to enable these analyses. Our sources are indicated below each analysis.

                The data we gather is available on our [Github repository](https://github.com/pschaus/covidbe-opendata),
                along with the software needed to produce it. Feel free to reuse!
            """),
        html.H3(["Contributing to the project"]),
        dcc.Markdown("""
                Whether you are a doctor, a data analysis specialist, or a member of the general public, you 
                may have
                - questions that we may be able to answer with more data, 
                - some data that we could use (and open to the public!),
                - ideas of new analysis.

                If this is the case, don't hesitate to contact us by mail (see the [About page](/about)) or to go directly
                to our [Github page](https://github.com/pschaus/covidbe-opendata). 
                We gladly accept new contributions!
            """)
    ]


def display_about():
    return html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index")


index_menu = AppMenu('index', '', [
    AppLink("Home", '/index', display_index),
    AppLink("About", '/about', display_about)
], fake_menu=True)

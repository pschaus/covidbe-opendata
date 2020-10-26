import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.Re import plot_Re, plot_daily_exp_factor, plot_Re_div_n
from pages.sources import display_source_providers, source_sciensano, source_SI_modelRe
from pages import model_warning, get_translation, display_graphic
import urllib.parse
import re


def convert(text):
    def toimage(x):
        if x[1] and x[-2] == r'$':
            x = x[2:-2]
            img = "\n<img src='https://math.now.sh?from={}' style='display: block; margin: 0.5em auto;'>\n"
            return img.format(urllib.parse.quote_plus(x))
        else:
            x = x[1:-1]
            return r'![](https://math.now.sh?from={})'.format(urllib.parse.quote_plus(x))
    return re.sub(r'\${2}([^$]+)\${2}|\$(.+?)\$', lambda x: toimage(x.group()), text)




Markdown_text = r"""
We can also define $\beta$ and $\mu$ that are respectively the inflow and the outflow of infectious individuals per infectious capita. 
When the outflow is higher than the outflow, then $Re<1$.
An individual is expected to infect a number of $\frac{\beta}{\mu}$ secondary cases, which represents the $Re$.
"""

#formula_Re = r"""
#$Re = \frac{\beta}{\mu}$
#"""


Markdown_text = convert(Markdown_text)
#Markdown_text2 = convert(Markdown_text2)
#formula_Re = convert(formula_Re)


#app.layout = html.Div([
#    
#])

def display_Re():
    return [
        *model_warning(
        html.Iframe(src="https://www.youtube.com/embed/TXZW5Q7p2tk", style = dict(border=0), width ="100%", height ="600"),

        html.H2(gettext("Daily multiplicative factor")),
        html.P("The daily multiplicative factor gives the relative daily increase/decrease of positive cases. When >1, the strength of the epidemy is increasing, when <1, the strength of the epidemy is decreasing."),
        dbc.Row([
            dbc.Col(display_graphic(id='daily_exp_factor', figure=plot_daily_exp_factor(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.H2(gettext("Effective number of secondary infections (Re factor)")),
            html.P(
                """
                The concept of effective number of secondary infections per infection case Re is an interesting indicator to compute easily interpretable for everyone.
                When specific actions are taken to ensure protection and social distancing or when the number of immune persons grows up, Re is supposed to decrease.

                It should not be confused with R0 (pronounced, “R naught”) indicating how contagious the disease  is when everyone is susceptible.
                R0 directly depends on the nature of the infectious disease.
                """),
            html.P(
                """
                If Re is greater than one then the number of infected persons grows faster than the number of recovered or deceased persons and this leads to an outbreak of the epidemic. 
                It is thus crucial that the Re factor is not higher than 1 for a long period. 
                If Re is less than one then the outbreak will tend to  extinct because fewer and fewer people are infected."""),
        html.P(
                "As we only have access to the cases tested positive at time t (without knowing exactly when they are not active anymore), we have to make some hypotheses to estimate the Re:"),
        dcc.Markdown('''
    * if we consider that it takes n days for an active patient to recover (n is thus a parameter of our model), 
    * if we make a moving average over 7 days of the positive patients,
    * if we consider that the population that has developed is not significant (<<10\%-20\%), and
    * if we consider that the number of persons tested positive is proportional to the actual number of positive persons.
    '''),
        html.P("We can also visualize the Re factor:"),
        html.P("Here are the curves that we obtain since the lockdown in Belgium:"),
        dbc.Row([
            dbc.Col(display_graphic(id='Re', figure=plot_Re()[2],
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),


        html.H2(gettext("Additional visualisations")),
        dcc.Markdown(Markdown_text, dangerously_allow_html=True),

        #html.P("Here are the curves that we obtain since the lockdown in Belgium:"), 
        dbc.Row([
            dbc.Col(display_graphic(id='Re', figure=plot_Re()[0],
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(display_graphic(id='Re', figure=plot_Re()[1],
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        #html.P("The number of secondary infections Re can be understood as the exponential factor of the number of infected persons, with the specificity that the time scale for that exponential increase is related to the period of the infection. If we look at the exponential increase of active cases on a daily basis, we have to look at Re^(1/n)."),
        #dbc.Row([
        #    dbc.Col(display_graphic(id='daily_exp_factor_from_Re', figure=plot_Re_div_n(),
        #                      config=dict(locale=str(get_locale()))), className="col-12"),
        #]),

        display_source_providers(source_sciensano,source_SI_modelRe)
        )
    ]

def callback_Re(app):
    #app = dash.Dash(__name__)
    #mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
    #app.scripts.append_script({ 'external_url' : mathjax })

    @app.callback(
      dash.dependencies.Output('dynamic','children'),
     [dash.dependencies.Input('button','n_clicks')]
    )
    def addmath(n_clicks):
      if n_clicks:
        return '$$ x=1 $$'
      else:
        return None

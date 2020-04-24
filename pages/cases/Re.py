import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.Re import plot_Re, plot_daily_exp_factor#, plot_Re_div_n
from pages.sources import display_source_providers, source_sciensano, source_SI_modelRe
from pages import model_warning, get_translation

def display_Re():
    return [
        *model_warning(
html.H2(gettext("Effective number of secondary infections (Re factor)")),
        html.P("The term R0 (pronounced “R naught”) indicates how contagious an infectious disease is. R0 directly depends on the nature of the infectious disease. When specific actions are taken to ensure protection and social distancing, the concept of effective number of secondary infections Re is often used (even though sometimes stills referred to as R0)."),
        html.P("If Re is greater than one then the number of infected persons grows faster than the number of recovered or deceased persons and this leads to an outbreak of the epidemic. It is thus crucial that the Re factor is not higher than 1 for a long period. If Re is less than one then the outbreak will tend to  extinct because less and less people are infected."),
        html.P("As we only have access to the cases tested positive at time t (without knowing exactly when they are not active anymore), we have to make some hypotheses to estimate the Re:"), 
        dcc.Markdown('''
        * if we consider that it takes n days for an active patient to recover (n is thus a parameter of our model), 
        * if we make a moving average over 7 days of the positive patients, and
        * if we consider that the number of persons tested positive is proportional to the actual number of positive persons.
        '''), 
        html.P("Then here are the curves that we obtain since the lockdown in Belgium:"), 
        dbc.Row([
            dbc.Col(dcc.Graph(id='Re', figure=plot_Re(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='daily_exp_factor', figure=plot_daily_exp_factor(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
#        dbc.Row([
#            dbc.Col(dcc.Graph(id='daily_exp_factor_from_Re', figure=plot_Re_div_n(),
#                              config=dict(locale=str(get_locale()))), className="col-12"),
#        ]),
        display_source_providers(source_sciensano,source_SI_modelRe)
        )
    ]
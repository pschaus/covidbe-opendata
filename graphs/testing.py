import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np


from graphs import register_plot_for_embedding

df_testing = pd.read_csv('static/csv/be-covid-testing.csv')

def moving_average(a, n=1) :
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n-1] = ret[:n-1]/range(1,n)
    ret[n-1:] = ret[n - 1:] / n
    return ret


@register_plot_for_embedding("bart_plot_cases_testing")
def bart_plot_cases_testing():
    """
    bar plot cases and testing everyday
    """
    # ---------bar plot age groups death---------------------------

    test_bar = go.Bar(x=df_testing.DATE, y=df_testing.TESTS_ALL, name=gettext('#Tests'),marker_color="blue",legendgroup = "testing", showlegend = True)
    case_bar = go.Bar(x=df_testing.DATE, y=df_testing.CASES, name=gettext('#Cases'),marker_color="red",legendgroup = "cases", showlegend = True)

    line_test = go.Scatter(x=df_testing.DATE, y=moving_average(df_testing.TESTS_ALL.values, 7),
                           name=gettext('#Tests'),marker_color="blue",legendgroup = "testing", showlegend = False)
    case_test = go.Scatter(x=df_testing.DATE, y=moving_average(df_testing.CASES.values, 7), name=gettext('#Cases'),marker_color="red",legendgroup = "cases", showlegend = False)

    fig_testing = go.Figure(data=[test_bar, case_bar, line_test, case_test], layout=go.Layout(barmode='group'), )
    fig_testing.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                              title=gettext("Number of Tests and Cases each day"))

    fig_testing.update_layout(xaxis_title=gettext('Day'),
                              yaxis_title=gettext('Number of / Day'))

    fig_testing.update_layout(
        hovermode='x unified',
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear"}],
                        label="LINEAR",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log"}],
                        label="LOG",
                        method="relayout"
                    )
                ]),
            ),
        ])

    return fig_testing


@register_plot_for_embedding("plot_ration_cases_over_testing")
def plot_ration_cases_over_testing():
    """
    plot of the ration cases over testing everyday
    """
    fig = px.line(x=df_testing.DATE,y=df_testing.CASES/df_testing.TESTS_ALL, title=gettext("#Cases/#Tests each day"))
    fig.update_layout(xaxis_title=gettext('Day'),
                   yaxis_title=gettext('#Cases/#Tests'))
    return fig



@register_plot_for_embedding("plot_ration_cases_over_testing_smooth")
def plot_ration_cases_over_testing_smooth():
    """
    plot of the ration cases over testing everyday
    """

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_testing.DATE.values[7:], y=(moving_average(100*df_testing.CASES.values, 7) / moving_average(df_testing.TESTS_ALL.values, 7))[7:],
                    mode='lines',
                    name='cases / all tests (%)'))
    fig.add_trace(go.Scatter(x=df_testing.DATE.values[7:], y=(moving_average(100*df_testing.TESTS_ALL_POS.values, 7) / moving_average(df_testing.TESTS_ALL.values, 7))[7:],
                    mode='lines',
                    name='positive tests / all tests (%)'))


    fig.update_layout(xaxis_title=gettext('Day'),
                      yaxis_title=gettext('Positive rate %'), title=gettext("Positive rate % (avg over past 7 days)"))
    fig.update_layout(template="plotly_white")

    return fig


@register_plot_for_embedding("plot_cumulated_testing")
def plot_cumulated_testing():
    """
    plot of the cumulated tests cases of days everyday
    """
    fig = go.Figure(data=[go.Scatter(x=df_testing.DATE, y=df_testing.TESTS_ALL.cumsum(), name=gettext('Cumulated #Test')),
                          go.Scatter(x=df_testing.DATE, y=df_testing.CASES.cumsum(), name=gettext('Cumulated #Cases'))]
                    )
    fig.update_layout(xaxis_title=gettext('Day'),
                      yaxis_title=gettext('#Cases/#Tests'), title=gettext("Cumulated number of Tests and Cases"))
    fig.update_layout(template="plotly_white")
    return fig

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

df_testing = pd.read_csv('static/csv/be-covid-testing.csv')


def moving_average(a, n=1):
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n - 1] = ret[:n - 1] / range(1, n)
    ret[n - 1:] = ret[n - 1:] / n
    return ret


@register_plot_for_embedding("test_vs_case_increase")
def test_vs_case_increase():
    df_testing = pd.read_csv('static/csv/be-covid-testing.csv')

    tests = df_testing['TESTS_ALL'].rolling(7).sum().values[7:-4]
    cases = df_testing['CASES'].rolling(7).sum().values[7:-4]
    x = tests[1:] / tests[:-1]
    y = cases[1:] / cases[:-1]

    dates = df_testing.DATE[7:-4]

    fig = px.scatter(x=x, y=y, labels={'x': 'tests daily increase', 'y': 'case daily increase'})
    fig.add_trace(
        go.Scatter(x=x[-15:], y=y[-15:], text=dates[-15:], mode='markers', name="last 15 days", marker_color="red"))
    fig.add_trace(go.Scatter(x=x[210:250], y=y[210:250], text=dates[210:250], mode='markers', name="october",
                             marker_color="black"))

    xl = np.arange(min(x), max(x), 0.01)
    yl = xl
    fig.add_trace(go.Scatter(x=xl, y=yl, showlegend=False, line={'dash': 'dash'}))
    fig.update_layout(template="plotly_white")
    return fig


@register_plot_for_embedding("bart_plot_cases_testing")
def bart_plot_cases_testing():
    """
    bar plot cases and testing everyday
    """
    # ---------bar plot age groups death---------------------------

    test_bar = go.Bar(x=df_testing.DATE[:-4], y=df_testing.TESTS_ALL[:-4], name=gettext('#Tests'), marker_color="blue",
                      legendgroup="testing", showlegend=True)
    case_bar = go.Bar(x=df_testing.DATE, y=df_testing.CASES, name=gettext('#Cases'), marker_color="red",
                      legendgroup="cases", showlegend=True)

    test_bar_last = go.Bar(x=df_testing.DATE[-4:], y=df_testing.TESTS_ALL[-4:], name=gettext('#Tests Not Consolidated'),
                           marker_color="lightblue",
                           legendgroup="testing", showlegend=True)

    case_bar = go.Bar(x=df_testing.DATE[:-4], y=df_testing.CASES[:-4], name=gettext('#Cases'), marker_color="red",
                      legendgroup="cases", showlegend=True)

    case_bar_last = go.Bar(x=df_testing.DATE[-4:], y=df_testing.CASES[-4:], name=gettext('#Cases Not Consolidated'),
                           marker_color="pink",
                           legendgroup="cases", showlegend=True)

    line_test = go.Scatter(x=df_testing.DATE[:-4], y=df_testing.TESTS_ALL[:-4].rolling(7, center=True).mean(),
                           name=gettext('#Tests avg'), marker_color="blue", legendgroup="testing-avg", showlegend=True)

    line_case = go.Scatter(x=df_testing.DATE[:-4],
                           y=df_testing.CASES[:-4].rolling(7, center=True).mean(),

                           name=gettext('#Cases avg'),
                           marker_color="red", legendgroup="cases-avg", showlegend=True)

    fig = make_subplots(specs=[[{"secondary_y": True, }]], shared_yaxes='all', shared_xaxes='all')
    fig.add_trace(test_bar, secondary_y=False)
    fig.add_trace(test_bar_last, secondary_y=False)
    fig.add_trace(line_test, secondary_y=False)
    fig.add_trace(case_bar, secondary_y=True)
    fig.add_trace(case_bar_last, secondary_y=True)
    fig.add_trace(line_case, secondary_y=True)

    # Set y-axes titles
    fig.update_yaxes(title_text="#tests/day", secondary_y=False)
    fig.update_yaxes(title_text="#cases/day", secondary_y=True)

    fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                      title=gettext("Number of Tests and Cases each day"))

    fig.update_layout(
        hovermode='x unified',
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear", "yaxis2.type": "linear"}],
                        label="LINEAR",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log", "yaxis2.type": "log"}],
                        label="LOG",
                        method="relayout"
                    )
                ]),
            ),
        ])

    return fig



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

    fig.add_trace(go.Scatter(x=df_testing.DATE[:-4], y=100 * df_testing.TESTS_ALL_POS[:-4].rolling(7,
                                                                                         center=True).mean() / df_testing.TESTS_ALL.rolling(
        7, center=True).mean(),
                             mode='lines',
                             name='positive tests / all tests (%) avg',
                             marker_color="blue", legendgroup="two", showlegend=True))

    fig.add_trace(go.Scatter(x=df_testing.DATE, y=100 * df_testing.TESTS_ALL_POS / df_testing.TESTS_ALL,
                             mode='markers',
                             name='positive tests / all tests (%)',
                             marker_color="blue", legendgroup="twoa", showlegend=True))

    fig.update_layout(xaxis_title=gettext('Day'),
                      yaxis_title=gettext('Positive rate %'), title=gettext("Positive rate % (avg over past 7 days)"))
    fig.update_layout(template="plotly_white")

    fig.update_layout(
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

    return fig


@register_plot_for_embedding("plot_poscasesandtests")
def plot_positive_cases_tests():
    """
    plot of the ration cases over testing everyday
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_testing.DATE[:-4], y=100 * df_testing[:-4].CASES.rolling(7, center=True).mean(),
                             mode='lines',
                             name='positive cases avg',
                             marker_color="red", legendgroup="onea", showlegend=True))

    fig.add_trace(go.Scatter(x=df_testing.DATE[:-4], y=100 * df_testing.CASES[:-4],
                             mode='markers',
                             name='positive tests',
                             marker_color="red", legendgroup="oneb", showlegend=True))

    fig.add_trace(go.Scatter(x=df_testing.DATE[:-4], y=100 * df_testing.TESTS_ALL_POS[:-4].rolling(7, center=True).mean(),
                             mode='lines',
                             name='positive tests avg',
                             marker_color="blue", legendgroup="twoa", showlegend=True))

    fig.add_trace(go.Scatter(x=df_testing.DATE[:-4], y=100 * df_testing.TESTS_ALL_POS[:-4],
                             mode='markers',
                             name='positive tests',
                             marker_color="blue", legendgroup="twob", showlegend=True))

    fig.update_layout(xaxis_title=gettext('Day'),
                      yaxis_title=gettext('Number of'), title=gettext("Number of positive tests/cases"))
    fig.update_layout(template="plotly_white")

    fig.update_layout(
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

    return fig


@register_plot_for_embedding("plot_cumulated_testing")
def plot_cumulated_testing():
    """
    plot of the cumulated tests cases of days everyday
    """
    fig = make_subplots(specs=[[{"secondary_y": True, }]], shared_yaxes='all', shared_xaxes='all')

    fig.add_trace(
        go.Scatter(x=df_testing.DATE, y=df_testing.TESTS_ALL.cumsum(), name=gettext('Cumulated #Test')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_testing.DATE, y=df_testing.CASES.cumsum(), name=gettext('Cumulated #Cases')),
        secondary_y=True,
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="cumulated #tests", secondary_y=False)
    fig.update_yaxes(title_text="cumulated #cases", secondary_y=True)

    fig.update_layout(title=gettext("Cumulated number of Tests and Cases"))
    fig.update_layout(template="plotly_white")
    return fig



import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np


from graphs import register_plot_for_embedding

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import numpy as np
import io
import requests
from graphs import register_plot_for_embedding

df = pd.read_csv('static/csv/be-covid-provinces-all.csv')

df = df.groupby([df.DATE, df.REGION]).agg(
    {'CASES': ['sum'], 'TESTS_ALL': ['sum'], 'TESTS_ALL_POS': ['sum'], 'NEW_IN': ['sum']}).reset_index()
df.columns = df.columns.get_level_values(0)



def trace(region, log=False, div=1, mul=1):
    return go.Scatter(name=region,
                      x=df[df.REGION == region].DATE,
                      y=df[df.REGION == region].CASES.rolling(7).mean() / div * mul)


@register_plot_for_embedding("plot_relative_cases_region")
def plot_relative_cases():
    fig = go.Figure()
    brux_pop = 1218255
    wall_pop = 3645243
    flanders_pop = 6629143

    fig.add_trace(trace('Wallonia', div=wall_pop, mul=100000))
    fig.add_trace(trace('Flanders', div=flanders_pop, mul=100000))
    fig.add_trace(trace('Brussels', div=brux_pop, mul=100000))

    fig.update_layout(template="plotly_white", title="Number of cases/100000 habitants")
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

@register_plot_for_embedding("plot_relative_cases_region")
def plot_relative_cases():
    fig = go.Figure()
    brux_pop = 1218255
    wall_pop = 3645243
    flanders_pop = 6629143

    fig.add_trace(trace('Wallonia', div=wall_pop, mul=100000))
    fig.add_trace(trace('Flanders', div=flanders_pop, mul=100000))
    fig.add_trace(trace('Brussels', div=brux_pop, mul=100000))

    fig.update_layout(template="plotly_white", title="Number of cases/100000 habitants")
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


@register_plot_for_embedding("cases_relative_region")
def cases_relative_region():
    return plot_relative_cases()

@register_plot_for_embedding("positive_rate_region")
def positive_rate_region():
    df_pos = df.groupby([df.DATE,df.REGION]).agg({'TESTS_ALL': ['sum'],'TESTS_ALL_POS': ['sum']}).reset_index()
    df_pos.columns = df_pos.columns.get_level_values(0)
    df_pos['POSITIVE_RATE'] = 100*df_pos['TESTS_ALL_POS']/df_pos['TESTS_ALL']
    df_pos.sort_values(by=['DATE'], inplace=True, ascending=True)


    fig = go.Figure()
    #fig = px.line(x=df_pos.DATE,y=df_pos.POSITIVE_RATE,color=df.REGION)
    regions = ['Brussels','Flanders','Wallonia']
    plots = []
    for r in regions:
        dfr = df_pos[df_pos.REGION == r]
        plot = go.Scatter(x=dfr['DATE'], y=dfr['POSITIVE_RATE'].rolling(7).mean(),name=r)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))
    fig.update_layout(template="plotly_white", title="Positive Rate (%)")
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


@register_plot_for_embedding("number_of_test_per_inhabitant_region")
def number_of_test_per_inhabitant_region():
    df_pos = df.groupby([df.DATE, df.REGION]).agg({'TESTS_ALL': ['sum'], 'TESTS_ALL_POS': ['sum']}).reset_index()
    df_pos.columns = df_pos.columns.get_level_values(0)
    df_pos['POSITIVE_RATE'] = df_pos['TESTS_ALL_POS'] / df_pos['TESTS_ALL']
    df_pos.sort_values(by=['DATE'], inplace=True, ascending=True)

    pop = {'Brussels': 1218255, 'Flanders': 6629143, 'Wallonia': 3645243}

    fig = go.Figure()
    regions = ['Brussels', 'Flanders', 'Wallonia']
    plots = []
    for r in regions:
        dfr = df_pos[df_pos.REGION == r]
        plot = go.Scatter(x=dfr['DATE'], y=(100000*dfr['TESTS_ALL'] / pop[r]).rolling(7).mean(), name=r)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))
    fig.update_layout(template="plotly_white", title="Number of tests per 100K inhabitants")
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


@register_plot_for_embedding("ratio_case_hospi_region")
def ratio_case_hospi_region():
    barmode = 'stack'  # group
    # bar plot with bars per age groups
    bars = []
    regions = sorted(df.REGION.unique())

    idx = pd.date_range(df.DATE.min(), df.DATE.max())

    for r in regions:
        df_r = df.loc[df['REGION'] == r]
        n = 200
        plot = go.Scatter(x=df_r.DATE[-n:-4],
                          y=(df_r['NEW_IN'][-n:-4].rolling(7).mean() / df_r['CASES'][-n:-4].rolling(7).mean()).rolling(
                              7).mean(), name=r)

        bars.append(plot)

    fig = go.Figure(data=bars,
                    layout=go.Layout(barmode='group'), )
    fig.update_layout(template="plotly_white", height=500, barmode=barmode, margin=dict(l=0, r=0, t=30, b=0), )

    fig.update_layout(template="plotly_white", title="RATIO NEW_IN Hospital (avg 7 days) / CASES (avg 7 days)")
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
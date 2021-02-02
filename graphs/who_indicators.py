import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding


def df_hospi_death():
    df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')
    idx = pd.date_range(df_hospi.DATE.min(), df_hospi.DATE.max())
    df_hospi = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'TOTAL_IN_ICU': 'sum', 'NEW_IN': 'sum'})
    df_hospi.index = pd.DatetimeIndex(df_hospi.index)
    df_hospi = df_hospi.reindex(idx, fill_value=0)

    df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)
    idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
    df_mortality = df_mortality.groupby(['DATE']).agg({'DEATHS': 'sum'})
    df_mortality.index = pd.DatetimeIndex(df_mortality.index)
    df_mortality = df_mortality.reindex(idx, fill_value=0)

    df = df_mortality.merge(df_hospi, how='left', left_index=True, right_index=True)

    df = df[df.index >= '2020-03-15']
    return df


import numpy as np


def moving_average(a, n=1):
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n - 1] = ret[:n - 1] / range(1, n)
    ret[n - 1:] = ret[n - 1:] / n
    return ret


df = df_hospi_death()


def add_rectangle(fig, x1, y1, x2, y2, color):
    fig.add_shape(
        type="rect",
        x0=x1,
        y0=y1,
        x1=x2,
        y1=y2,
        fillcolor=color,
        opacity=0.5,
        layer="below",
        line_width=0,
    )


def add_text(fig, x, y, text):
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        align='center',
        showarrow=False,
        font=dict(size=16),
        yanchor='top',
    )


@register_plot_for_embedding("death_oms")
def death_oms():
    death_bar = go.Bar(x=df.index, y=df.DEATHS, name=gettext('#Daily Covid Deaths'), marker_color="red",
                       legendgroup="death", showlegend=False)
    death_smooth = go.Scatter(x=df.index, y=df.DEATHS.rolling(14).sum() / 2 / 115, name=("#Daily Covid Deaths"),
                              marker_color="blue", legendgroup="death", showlegend=False)

    fig = go.Figure(data=[death_smooth], layout=go.Layout(barmode='group'))

    # Mortalité = Nombre de décès attribués à la COVID-19 pour 100 000 habitants et par semaine (moyenne sur deux semaines)

    fig.update_layout(template="plotly_white", title="WHO Mortality Index")
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
    add_rectangle(fig, df.index.min(), 0, df.index.max(), 1, "#fef0d9")
    add_rectangle(fig, df.index.min(), 1, df.index.max(), 2, "#fdcc8a")
    add_rectangle(fig, df.index.min(), 2, df.index.max(), 5, "#fc8d59")
    add_rectangle(fig, df.index.min(), 5, df.index.max(), 17, "#d7301f")
    add_text(fig, "2020-03-25", 1, "TC1")
    add_text(fig, "2020-03-25", 2, "TC2")
    add_text(fig, "2020-03-25", 3, "TC3")
    add_text(fig, "2020-03-25", 6, "TC4")

    return fig


@register_plot_for_embedding("newin_oms")
def newin_oms():
    newin_smooth = go.Scatter(x=df.index, y=df.NEW_IN.rolling(14).sum() / 2 / 115, name=("#OMS HOSPI"),
                              marker_color="blue", legendgroup="death", showlegend=False)

    fig = go.Figure(data=[newin_smooth], layout=go.Layout(barmode='group'))

    # Mortalité = Nombre de décès attribués à la COVID-19 pour 100 000 habitants et par semaine (moyenne sur deux semaines)

    fig.update_layout(template="plotly_white", title="WHO Hospitalization Index")
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
    add_rectangle(fig, df.index.min(), 0, df.index.max(), 5, "#fef0d9")
    add_rectangle(fig, df.index.min(), 5, df.index.max(), 10, "#fdcc8a")
    add_rectangle(fig, df.index.min(), 10, df.index.max(), 30, "#fc8d59")
    add_rectangle(fig, df.index.min(), 30, df.index.max(), 40, "#d7301f")
    add_text(fig, "2020-03-25", 3, "TC1")
    add_text(fig, "2020-03-25", 8, "TC2")
    add_text(fig, "2020-03-25", 15, "TC3")
    add_text(fig, "2020-03-25", 33, "TC4")

    return fig





@register_plot_for_embedding("cases_oms")
def cases_oms():
    df = pd.read_csv('static/csv/be-covid-provinces-all.csv')
    df = df.groupby([df.DATE]).agg(
        {'CASES': ['sum'], 'TESTS_ALL': ['sum'], 'TESTS_ALL_POS': ['sum'], 'NEW_IN': ['sum']}).reset_index()
    df.columns = df.columns.get_level_values(0)
    cases_smooth = go.Scatter(x=df.DATE, y=df.CASES.rolling(14).sum() / 2 / 115, name=("#OMS CASES"),
                              marker_color="blue", legendgroup="death", showlegend=False)

    fig = go.Figure(data=[cases_smooth], layout=go.Layout(barmode='group'))

    # Mortalité = Nombre de décès attribués à la COVID-19 pour 100 000 habitants et par semaine (moyenne sur deux semaines)

    fig.update_yaxes(range=[0, 300])
    fig.update_layout(template="plotly_white", title="WHO Cases Index")
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
    add_rectangle(fig, df.DATE.min(), 0, df.DATE.max(), 20, "#fef0d9")
    add_rectangle(fig, df.DATE.min(), 20, df.DATE.max(), 50, "#fdcc8a")
    add_rectangle(fig, df.DATE.min(), 50, df.DATE.max(), 150, "#fc8d59")
    add_rectangle(fig, df.DATE.min(), 150, df.DATE.max(), 900, "#d7301f")
    add_text(fig, "2020-03-25", 15, "TC1")
    add_text(fig, "2020-03-25", 40, "TC2")
    add_text(fig, "2020-03-25", 100, "TC3")
    add_text(fig, "2020-03-25", 250, "TC4")

    return fig


@register_plot_for_embedding("posrate_oms")
def posrate_oms():
    df = pd.read_csv('static/csv/be-covid-provinces-all.csv')
    df = df.groupby([df.DATE]).agg(
        {'CASES': ['sum'], 'TESTS_ALL': ['sum'], 'TESTS_ALL_POS': ['sum'], 'NEW_IN': ['sum']}).reset_index()
    df.columns = df.columns.get_level_values(0)
    posrate_smooth = go.Scatter(x=df.DATE, y=100 * df.TESTS_ALL_POS.rolling(14).sum() / df.TESTS_ALL.rolling(14).sum(),
                                name=("#OMS CASES"), marker_color="blue", legendgroup="death", showlegend=False)

    fig = go.Figure(data=[posrate_smooth], layout=go.Layout(barmode='group'))

    fig.update_yaxes(range=[0, 30])
    fig.update_layout(template="plotly_white", title="WHO Positive Rate Index (%)")
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
    add_rectangle(fig, df.DATE.min(), 0, df.DATE.max(), 2, "#fef0d9")
    add_rectangle(fig, df.DATE.min(), 2, df.DATE.max(), 5, "#fdcc8a")
    add_rectangle(fig, df.DATE.min(), 5, df.DATE.max(), 20, "#fc8d59")
    add_rectangle(fig, df.DATE.min(), 20, df.DATE.max(), 40, "#d7301f")
    add_text(fig, "2020-03-25", 2, "TC1")
    add_text(fig, "2020-03-25", 5, "TC2")
    add_text(fig, "2020-03-25", 10, "TC3")
    add_text(fig, "2020-03-25", 23, "TC4")

    return fig





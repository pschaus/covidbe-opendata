

import plotly.express as px

import plotly.graph_objs as go
from flask_babel import gettext
from datetime import datetime, date
import plotly.graph_objs as go
import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation
import numpy as np
from graphs import register_plot_for_embedding

from datetime import datetime



df_week85 = pd.read_csv("static/csv/weekly_mortality_85+.csv")
df_week_all = pd.read_csv("static/csv/weekly_mortality_all.csv")

df = pd.read_csv("static/csv/mortality_statbel.csv")

df_ag = df.groupby([df.DT_DATE,df.CD_AGEGROUP]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
df_ag.columns = df_ag.columns.get_level_values(0)

df = df.groupby([df.DT_DATE]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
df.columns = df.columns.get_level_values(0)


age_groups = ['0-24', '25-44', '45-64', '65-74', '75-84', '85+']


def moving_average(a, n=1):
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n - 1] = ret[:n - 1] / range(1, n)
    ret[n - 1:] = ret[n - 1:] / n
    return ret


def sin_fit_math(x, y):
    import numpy as np
    from scipy.optimize import curve_fit

    def sin_func(x, a, b, c, d):
        return a * np.sin(b * x + c) + d

    xx = np.arange(0, len(y), 1)
    popt, pcov = curve_fit(sin_func, xx[:5 * 365], y[:5 * 365], p0=(50, 0.017, 1, 300))
    # popt, pcov = curve_fit(sin_func, xx,y, p0=(50, 0.017, 1, 300))
    yy = sin_func(xx, *popt)
    return yy


def sin_fit(x, y, title):
    yy = sin_fit_math(x, y)
    sin_line = go.Scatter(
        x=x,
        y=yy,
        mode='lines',
        name='sin fit model ' + title
    )
    line = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='7 day average ' + title
    )

    return [line, sin_line]





def daily_death_all():
    plots = sin_fit(df.DT_DATE, moving_average(df.MS_NUM_DEATH.values, 7), "all pop")

    fig = go.Figure(
        data=plots,
        layout=go.Layout(
            title=go.layout.Title(text="Daily Mortality Belgium"),
            height=600
        ),

    )
    fig.update_layout(template="plotly_white")

    fig.update_layout(yaxis=dict(range=[0, 620]))
    return fig

def daily_death_all_deviation_sin():
    x = df.DT_DATE
    y = moving_average(df.MS_NUM_DEATH.values,7)

    yy =  sin_fit_math(x,y)

    relative = ((y-yy)/yy)*100

    col = np.where(relative<0, 'green', 'red')

    # Plot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(name='Deviation%',
               x=x,
               y=relative,
               marker_color=col))
    fig.update_layout(barmode='stack')

    fig.update_layout(template="plotly_white",title="Relative Deviation to the sinusoidal fit in %")

    return fig


def daily_death_ag():
    plots = []

    for ag in age_groups:
        df_ag_ = df_ag.loc[df_ag['CD_AGEGROUP'] == ag]
        plots = plots + sin_fit(df_ag_.DT_DATE, moving_average(df_ag_.MS_NUM_DEATH.values, 7), str(ag))

    fig = go.Figure(
        data=plots,
        layout=go.Layout(
            title=go.layout.Title(text="Daily Mortality Belgium by Age Group"),
            height=600
        ),

    )
    fig.update_layout(template="plotly_white")
    #fig.update_layout(yaxis=dict(range=[0, 300]))
    return fig


def death_85plus_hist():
    fig = px.line(df_week85, x="week", y="tot", color='year')

    fig.update_layout(xaxis_title='Week',
                      yaxis_title='#deaths 85+')
    return fig


def death_hist():
    fig = px.line(df_week_all, x="week", y="tot", color='year')

    fig.update_layout(xaxis_title='Week',
                      yaxis_title='#deaths')
    return fig

def death_85plus_hist_cum():
    def x(year):
        return df_week85[df_week85.year == year].week

    def y(year):
        return df_week85[df_week85.year == year].tot.cumsum()

    fig = go.Figure(data=[go.Scatter(x=x(2015), y=y(2015), name=gettext('2015')),
                          go.Scatter(x=x(2017), y=y(2017), name=gettext('2017')),
                          go.Scatter(x=x(2018), y=y(2018), name=gettext('2018')),
                          go.Scatter(x=x(2020), y=y(2020), name=gettext('2020')), ])

    fig.update_layout(xaxis_title='Week',
                      yaxis_title='cumulated #deaths 85+')
    return fig


def death_plus_hist_cum():
    def x(year):
        return df_week_all[df_week_all.year == year].week

    def y(year):
        return df_week_all[df_week_all.year == year].tot.cumsum()

    fig = go.Figure(data=[go.Scatter(x=x(2015), y=y(2015), name=gettext('2015')),
                          go.Scatter(x=x(2016), y=y(2016), name=gettext('2016')),
                          go.Scatter(x=x(2017), y=y(2017), name=gettext('2017')),
                          go.Scatter(x=x(2018), y=y(2018), name=gettext('2018')),
                          go.Scatter(x=x(2019), y=y(2019), name=gettext('2019')),
                          go.Scatter(x=x(2020), y=y(2020), name=gettext('2020')), ])

    fig.update_layout(xaxis_title='Week',
                      yaxis_title='cumulated #deaths all population')
    return fig

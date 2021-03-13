
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

from graphs import register_plot_for_embedding

from datetime import datetime



df_week85 = pd.read_csv("static/csv/weekly_mortality_85+.csv")
df_week_all = pd.read_csv("static/csv/weekly_mortality_all.csv")

df = pd.read_csv("static/csv/mortality_statbel.csv")

df_ag = df.groupby([df.DT_DATE ,df.CD_AGEGROUP]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
df_ag.columns = df_ag.columns.get_level_values(0)


df = df.groupby([df.DT_DATE ,df.NR_YEAR]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
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




@register_plot_for_embedding("daily_death_all")
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


@register_plot_for_embedding("daily_death_all_deviation_sin")
def daily_death_all_deviation_sin():
    x = df.DT_DATE
    y = moving_average(df.MS_NUM_DEATH.values ,7)

    yy =  sin_fit_math(x ,y)

    relative = (( y -yy ) /yy ) *100

    col = np.where(relative <0, 'green', 'red')

    # Plot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(name='Deviation%',
               x=x,
               y=relative,
               marker_color=col))
    fig.update_layout(barmode='stack')
    fig.update_xaxes(range=['2020-1-1', max(x)])
    fig.update_layout(template="plotly_white" ,title="Relative Deviation to the sinusoidal fit in %")

    return fig

@register_plot_for_embedding("daily_death_ag")
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
    # fig.update_layout(yaxis=dict(range=[0, 300]))
    return fig



@register_plot_for_embedding("death_plus_hist_cum")
def death_plus_hist_cum():
    def x(year):
        return df[df.NR_YEAR == year].DT_DATE

    def y(year):
        return df[df.NR_YEAR == year].MS_NUM_DEATH.cumsum()

    fig = go.Figure(data=[go.Scatter(y=y(2015), name=gettext('2015')),
                          go.Scatter(y=y(2016), name=gettext('2016')),
                          go.Scatter(y=y(2017), name=gettext('2017')),
                          go.Scatter(y=y(2018), name=gettext('2018')),
                          go.Scatter(y=y(2019), name=gettext('2019')),
                          go.Scatter(y=y(2020), name=gettext('2020')),
                          go.Scatter(y=y(2021), name=gettext('2020'))])

    fig.update_layout(xaxis_title='#Days since 1st of January',
                      yaxis_title='cumulated #deaths all population')
    fig.update_layout(template="plotly_white")
    return fig


@register_plot_for_embedding("death_cumsum_comparison_2021")
def death_cum_january_2021():

    years = [2015 ,2016 ,2017 ,2018 ,2019 ,2020, 2021]


    def y(year):
        return df[df.NR_YEAR == year].MS_NUM_DEATH.cumsum()

    n = len(y(2021).values)
    values = [y(a).values[ min(n -1,364)] for a in years]

    fig = px.bar(x=years, y=values ,labels={"x" :"" ,"y" :""})
    fig.update_layout(template="plotly_white",
                      title="Total deaths since 1st of January at day  " +str(n) ,)
    return fig



@register_plot_for_embedding("death_cumsum_comparison")
def death_cum_january():

    years = [2015 ,2016 ,2017 ,2018 ,2019 ,2020]


    def y(year):
        return df[df.NR_YEAR == year].MS_NUM_DEATH.cumsum()

    n = len(y(2020).values)
    values = [y(a).values[ min(n -1,364)] for a in years]

    fig = px.bar(x=years, y=values ,labels={"x" :"" ,"y" :""})
    fig.update_layout(template="plotly_white",
                      title="Total deaths since 1st of January at day  " +str(n) ,)
    return fig


@register_plot_for_embedding("death_cumsum_comparison_excess")
def death_cum_january_additional():

    years = [2015 ,2016 ,2017 ,2018 ,2019]


    def y(year):
        return df[df.NR_YEAR == year].MS_NUM_DEATH.cumsum()

    n = len(y(2020).values)
    values = [(y(2020).values[ min(n -1,364) ] -y(a).values[ min(n -1,364)]) for a in years]

    fig = px.bar(x=years, y=values ,labels={"x" :"" ,"y" :""})
    fig.update_layout(template="plotly_white",
                      title="Additional deaths of 2020 since 1st of January at day  " +str(n) ,)
    return fig
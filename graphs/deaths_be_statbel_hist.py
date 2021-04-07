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
from plotly.subplots import make_subplots


from graphs import register_plot_for_embedding

from datetime import datetime

df_week85 = pd.read_csv("static/csv/weekly_mortality_85+.csv")
df_week_all = pd.read_csv("static/csv/weekly_mortality_all.csv")

df = pd.read_csv("static/csv/mortality_statbel.csv")

df_ag = df.groupby([df.DT_DATE, df.CD_AGEGROUP]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
df_ag.columns = df_ag.columns.get_level_values(0)

df = df.groupby([df.DT_DATE, df.NR_YEAR]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
df.columns = df.columns.get_level_values(0)

age_groups = ['0-24', '25-44', '45-64', '65-74', '75-84', '85+']



def all_death():


    df = pd.read_csv("static/csv/mortality_statbel.csv")


    df_ag = df.groupby([df.DT_DATE, df.CD_AGEGROUP]).agg({'MS_NUM_DEATH': ['sum']}).reset_index()
    df_ag.columns = df_ag.columns.get_level_values(0)

    df_ag.rename(columns={'MS_NUM_DEATH':'DEATHS_ALL','CD_AGEGROUP':'AGEGROUP','DT_DATE':'DATE'}, inplace=True)

    start_date = '2020-03-17'
    end_date = df_ag.DATE.max()

    df_ag = df_ag[df_ag.DATE >= start_date]
    df_ag = df_ag[df_ag.DATE <= end_date]

    age_groups = ['0-24', '25-44', '45-64', '65-74', '75-84', '85+']

    df_covid = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)
    df_covid = df_covid.groupby([df_covid.DATE, df_covid.AGEGROUP]).agg({'DEATHS': ['sum']}).reset_index()
    df_covid.columns = df_covid.columns.get_level_values(0)
    df_covid.rename(columns={'DEATHS':'DEATHS_COVID'}, inplace=True)
    df_covid = df_covid[df_covid.DATE >= start_date]
    df_covid = df_covid[df_covid.DATE <= end_date]


    df_all = pd.merge(df_covid, df_ag, left_on=['AGEGROUP','DATE'], right_on=['AGEGROUP','DATE'], how='outer')

    df_all.fillna(0,inplace=True)
    return df_all


df_all = all_death()





def death_decompose(fig, row, col, ag, show_legend=False, groupnorm=''):
    df_ag = df_all.loc[df_all['AGEGROUP'] == ag]
    fig.add_trace(go.Scatter(x=df_ag.DATE, y=(df_ag.DEATHS_ALL - df_ag.DEATHS_COVID).abs(), showlegend=show_legend,
                             name="non covid",
                             legendgroup=ag, stackgroup='one', line=dict(width=0.5), mode='lines', marker_color="blue",
                             groupnorm=groupnorm), row, col)
    fig.add_trace(go.Scatter(x=df_ag.DATE, y=df_ag.DEATHS_COVID, showlegend=show_legend, name="covid",
                             legendgroup=ag, stackgroup='one', line=dict(width=0.5), mode='lines', marker_color="red",
                             groupnorm=groupnorm), row, col)


def death_decompose(fig, row, col, ag, show_legend=False):
    df_ag = df_all.loc[df_all['AGEGROUP'] == ag]
    fig.add_trace(go.Scatter(x=df_ag.DATE, y=(df_ag.DEATHS_ALL - df_ag.DEATHS_COVID).abs(), showlegend=show_legend,
                             name="non covid",
                             legendgroup=ag, stackgroup='one', line=dict(width=0.5), mode='lines', marker_color="blue",
                             groupnorm=""), row, col)
    fig.add_trace(go.Scatter(x=df_ag.DATE, y=df_ag.DEATHS_COVID, showlegend=show_legend, name="covid",
                             legendgroup=ag, stackgroup='one', line=dict(width=0.5), mode='lines', marker_color="red",
                             groupnorm=""), row, col)

@register_plot_for_embedding("fig__ag_death_decompose_time")
def fig_ag_death_decompose_time():
    fig = make_subplots(rows=6, cols=1, subplot_titles=('0-24', '25-44', '45-64', '65-74', '75-84', '85+'))
    death_decompose(fig, 1, 1, '0-24', show_legend=True)
    death_decompose(fig, 2, 1, '25-44', show_legend=False)
    death_decompose(fig, 3, 1, '45-64', show_legend=False)
    death_decompose(fig, 4, 1, '65-74', show_legend=False)
    death_decompose(fig, 5, 1, '75-84', show_legend=False)
    death_decompose(fig, 6, 1, '85+', show_legend=False)

    fig.update_layout(template="plotly_white", height=1000, margin=dict(l=50, r=50, t=50, b=50),
                      title="BE total deaths: covid vs non-covid ")

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                buttons=list([
                    dict(
                        args=[{"groupnorm": ""}],
                        label="absolute",
                        method="restyle"
                    ),
                    dict(
                        args=[{"groupnorm": "percent"}],
                        label="percent",
                        method="restyle"
                    )
                ]),
            ),
        ])

    return fig

@register_plot_for_embedding("fig_ag_death_decompose_aggregate")
def fig_ag_death_decompose_aggregate():
    df_ag = df_all.groupby([df_all.AGEGROUP]).agg({'DEATHS_ALL': ['sum'], 'DEATHS_COVID': ['sum']}).reset_index()
    df_ag.columns = df_ag.columns.get_level_values(0)
    df_ag = df_ag[df_ag.AGEGROUP != 'NA']

    fig = go.Figure(data=[
        go.Scatter(name='non-covid', x=df_ag.AGEGROUP, y=df_ag.DEATHS_ALL - df_ag.DEATHS_COVID, stackgroup='one',
                   groupnorm=""),
        go.Scatter(name='covid', x=df_ag.AGEGROUP, y=df_ag.DEATHS_COVID, stackgroup='one', groupnorm="")
    ])
    fig.update_layout(template="plotly_white", margin=dict(l=50, r=50, t=50, b=50),
                      title="BE total deaths: covid vs non-covid since covid outbreak")

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                buttons=list([
                    dict(
                        args=[{"groupnorm": ""}],
                        label="absolute",
                        method="restyle"
                    ),
                    dict(
                        args=[{"groupnorm": "percent"}],
                        label="percent",
                        method="restyle"
                    )
                ]),
            ),
        ])

    return fig




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


def sin_fit(x, y, title,color="blue",points=True):
    yy = sin_fit_math(x, y.values)

    sin_line = go.Scatter(
        x=x,
        y=yy,
        mode='lines',
        name='sin fit model ' + title,
        legendgroup=title,
        marker_color="grey"
    )

    avgline = go.Scatter(
        x=x,
        y=y.rolling(7, center=True).mean().values,
        mode='lines',
        name='7 day average ' + title,
        legendgroup=title,
        marker_color=color
    )
    res = [sin_line, avgline]
    if points:
        line = go.Scatter(
            x=x,
            y=y.values,
            mode='markers',
            name='daily ' + title,
            legendgroup=title,
            marker_color=color
        )
        res.append(line)
    return [sin_line, avgline]


@register_plot_for_embedding("daily_death_all")
def daily_death_all():
    plots = sin_fit(df.DT_DATE, df.MS_NUM_DEATH, "all pop")

    fig = go.Figure(
        data=plots,
        layout=go.Layout(
            title=go.layout.Title(text="Daily Mortality Belgium"),
            height=600
        ),

    )
    fig.update_layout(template="plotly_white")

    fig.update_layout(xaxis_range=['2020-01-01', datetime.today().strftime('%Y-%m-%d')])

    fig.update_layout(yaxis=dict(range=[0, 620]))
    return fig


@register_plot_for_embedding("daily_death_all_deviation_sin")
def daily_death_all_deviation_sin():
    x = df.DT_DATE


    yy =  sin_fit_math(x ,df.MS_NUM_DEATH.values)

    relative = (( df.MS_NUM_DEATH.values -yy ) /yy ) *100

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
    cols = px.colors.qualitative.Plotly
    i = 0
    for ag in age_groups:
        df_ag_ = df_ag.loc[df_ag['CD_AGEGROUP'] == ag]
        plots = plots + sin_fit(df_ag_.DT_DATE, df_ag_.MS_NUM_DEATH, str(ag),color=cols[i],points=False)
        i += 1

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


@register_plot_for_embedding("daily_death_ag_relative")
def daily_death_ag_relative():
    traces = []
    cols = px.colors.qualitative.Plotly
    i = 0
    for ag in age_groups:
        df_ag_ = df_ag.loc[df_ag['CD_AGEGROUP'] == ag]

        trace = dict(x=df_ag_.DT_DATE, y=df_ag_.MS_NUM_DEATH.rolling(7, center=True).mean(), mode='lines',
                     line=dict(width=0.5),
                     stackgroup='one', groupnorm='percent', name=ag,showlegend=True)
        traces.append(trace)

        i += 1



    fig = go.Figure(data=traces)

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                buttons=list([
                    dict(
                        args=[{"groupnorm": ""}],
                        label="absolute",
                        method="restyle"
                    ),
                    dict(
                        args=[{"groupnorm": "percent"}],
                        label="percent",
                        method="restyle"
                    )
                ]),
            ),
        ])

    # Edit the layout
    fig.update_layout(template="plotly_white", margin=dict(l=50, r=50, t=50, b=50),
                      title='Age group total death',
                      xaxis_title='Date',
                      yaxis_title='Percentage')
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
                          go.Scatter(y=y(2021), name=gettext('2021'))])

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
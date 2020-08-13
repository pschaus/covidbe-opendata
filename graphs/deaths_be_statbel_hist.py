

import plotly.express as px

import plotly.graph_objs as go
from flask_babel import gettext


from datetime import datetime

import pandas

df_week85 = pandas.read_csv("static/csv/weekly_mortality_85+.csv")
df_week_all = pandas.read_csv("static/csv/weekly_mortality_all.csv")

def death_85plus_hist():
    fig = px.line(df_week85, x="week", y="tot", color='year')

    fig.update_layout(xaxis_title='Week',
                      yaxis_title='#deaths 85+')
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

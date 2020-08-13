

import plotly.express as px

import plotly.graph_objs as go
from flask_babel import gettext


from datetime import datetime

import pandas

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
df = pandas.read_csv("static/csv/mortality_statbel.csv",parse_dates=['DT_DATE'], date_parser=dateparse)



df.dropna(thresh=1,inplace=True)

def week(date):
    return date.isocalendar()[1]


df['week'] = df.apply(lambda x: week(x['DT_DATE']), axis=1)



df_week85 = df.groupby(['NR_YEAR', 'week', 'CD_AGEGROUP'])["MS_NUM_DEATH"].sum().reset_index()
df_week85.rename(columns={"MS_NUM_DEATH": "tot", "NR_YEAR": "year", "CD_AGEGROUP": "age"}, inplace=True)
df_week85 = df_week85.loc[(df_week85['age'] == '85+')]


df_week_all = df.groupby(['NR_YEAR', 'week'])["MS_NUM_DEATH"].sum().reset_index()
df_week_all.rename(columns={"MS_NUM_DEATH": "tot", "NR_YEAR": "year"}, inplace=True)


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

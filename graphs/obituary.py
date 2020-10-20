import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import urllib.request, json

from graphs import register_plot_for_embedding

start = '03-15'

end = '10-18'



def necro_count_per_day(df, year):
    necro_count = df.groupby(['date'])['date'].agg(['count'])
    necro_count.reset_index(level=0, inplace=True)

    basedate = pd.Timestamp(f'{year}-{start}')
    necro_count['days'] = necro_count.apply(lambda x: (pd.to_datetime(x.date) - basedate).days, axis=1)

    mask = (necro_count['date'] >= f'{year}-{start}') & (necro_count['date'] <= f'{year}-{end}')
    necro_count = necro_count.loc[mask]

    necro_count.reset_index(level=0, inplace=True)

    return necro_count


def get_df_im(year):
    necro = pd.read_csv(f'static/csv/inmemoriam_{year}.csv')
    return necro_count_per_day(necro, year)


def get_df_dansnopensees(year):
    necro = pd.read_csv(f'static/csv/dansnopensees.csv')
    return necro_count_per_day(necro, year)


def get_df_sudpresse(year):
    necro = pd.read_csv(f'static/csv/necrosudpresse.csv')
    return necro_count_per_day(necro, year)


def get_df_avisdecesfr(year):
    necro = pd.read_csv(f'static/csv/avisdedecesfr_{year}.csv')
    return necro_count_per_day(necro, year)


df2019sp = get_df_sudpresse('2019')
df2020sp = get_df_sudpresse('2020')
df2019im = get_df_im('2019')
df2020im = get_df_im('2020')
df2019dp = get_df_dansnopensees('2019')
df2020dp = get_df_dansnopensees('2020')


df2019totbe = pd.DataFrame(
    [df2019sp['date'], df2019sp['days'], df2019sp['count'] + df2019im['count'] + df2019dp['count']]).transpose()
df2020totbe = pd.DataFrame(
    [df2020sp['date'], df2020sp['days'], df2020sp['count'] + df2020im['count'] + df2020dp['count']]).transpose()
convert_dict = {'count': int, 'days': int}


df2019totbe.dropna(inplace=True)
df2019totbe = df2019totbe.astype(convert_dict)
df2020totbe.dropna(inplace=True)
df2020totbe = df2020totbe.astype(convert_dict)


df2019av = get_df_avisdecesfr('2019')
df2020av = get_df_avisdecesfr('2020')


def plot(df2019, df2020, website):
    start_covid = '03-10'
    mask2019 = (df2019['date'] >= f'2019-{start_covid}') & (df2019['date'] <= f'2019-{end}')
    mask2020 = (df2020['date'] >= f'2020-{start_covid}') & (df2019['date'] <= f'2020-{end}')
    df2019 = df2019.loc[mask2019]
    df2020 = df2020.loc[mask2020]
    fig = go.Figure(data=[go.Scatter(x=df2019.days, y=df2019['count'].cumsum(), name='2019'),
                          go.Scatter(x=df2020.days, y=df2020['count'].cumsum(), name='2020'),
                          ])
    fig.update_layout(xaxis_title=gettext('Date'),
                      yaxis_title=gettext('#Deaths'),
                      xaxis=dict(tickmode='array', tickvals=df2019['days'][0::5], ticktext=df2019['date'][0::5]),
                      title=gettext("Cumulated Deaths on {website}").format(website=website), height=500)

    return fig



@register_plot_for_embedding("obituary_inmemoriam")
def inmemoriam_plot():
    return plot(df2019im, df2020im, "inmemoriam.be")

@register_plot_for_embedding("obituary_sudpresse")
def sudpresse_plot():
    return plot(df2019sp, df2020sp, "necro.sudpresse.be")

@register_plot_for_embedding("obituary_dansnospensees.be")
def dansnospensees_plot():
    return plot(df2019dp, df2020dp, "dansnopensees.be")

@register_plot_for_embedding("obituary_allbe.be")
def allbeobituary_plot():
    return plot(df2019totbe, df2020totbe, gettext("All belgian website, summed"))

@register_plot_for_embedding("obituary_avideces.fr")
def avideces_plot():
    return plot(df2019av, df2020av, "avisdeces.fr")


horizon = 7


def rolling_ratio_scatter(df2019, df2020, website):
    df2019r = df2019.rolling(horizon, min_periods=7).sum()
    df2020r = df2020.rolling(horizon, min_periods=7).sum()
    df2019r['date'] = df2019['date']

    return go.Scatter(x=df2019r.date, y=df2020r['count'] / df2019r['count'], name=website)

def ratio_scatter(df2019, df2020, website):
    df2020r = df2020.rolling(horizon, min_periods=7).sum()
    avg2019 = df2019['count'].mean()
    return go.Scatter(x=df2020.date, y=df2020r['count'] / (avg2019*7), name=website)


@register_plot_for_embedding("obituary_rolling_ratio")
def rolling_ratio_plot():
    fig = go.Figure(data=[rolling_ratio_scatter(df2019im, df2020im, "inmemoriam.be"),
                          rolling_ratio_scatter(df2019dp, df2020dp, "dansnopensees.be"),
                          rolling_ratio_scatter(df2019sp, df2020sp, "necro.sudpresse.be"),
                          rolling_ratio_scatter(df2019totbe, df2020totbe, gettext("All belgian website, summed"))])
    fig.update_layout(xaxis_title="",
                      yaxis_title=gettext('Ratio 2020/2019'),
                      title=gettext("Ratio reported death 2020/2019 with rolling horizon of 1 week"), height=500,
                      legend_orientation="h")
    fig.update_layout(
        xaxis_tickformat='%d/%m'
    )
    fig.update_layout(hovermode="x")
    return fig


@register_plot_for_embedding("obituary_rolling_ratio_fixed_division")
def ratio_plot():
    fig = go.Figure(data=[ratio_scatter(df2019im, df2020im, "inmemoriam.be"),
                          ratio_scatter(df2019dp, df2020dp, "dansnopensees.be"),
                          ratio_scatter(df2019sp, df2020sp, "necro.sudpresse.be"),
                          ratio_scatter(df2019totbe, df2020totbe, gettext("All belgian website, summed"))])
    fig.update_layout(xaxis_title="",
                      yaxis_title=gettext('Ratio 2020 / avg2019'),
                      title=gettext("Ratio reported death 2020/ avg 2019 with rolling horizon of 1 week"), height=500,
                      legend_orientation="h")
    fig.update_layout(
        xaxis_tickformat='%d/%m'
    )
    fig.update_layout(hovermode="x")
    return fig


def bar_daily(df2019, df2020, website):
    bar19 = go.Bar(x=df2019.index, y=df2019['count'], name='Number of deaths 2019')
    bar20 = go.Bar(x=df2020.index, y=df2020['count'], name='Number of deaths 2020')

    fig_bar_be = go.Figure(data=[bar19, bar20], )
    fig_bar_be.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                             xaxis=dict(tickmode='array', tickvals=df2019['days'][0::5], ticktext=df2019['date'][0::5]),
                             title=gettext(f"Daily deaths {website}"))
    return fig_bar_be


@register_plot_for_embedding("obituary_bar_plot_be")
def bar_plot_be():
    return bar_daily(df2019totbe,df2020totbe, gettext("All belgian website"))


@register_plot_for_embedding("obituary_bar_plot_fr")
def bar_plot_fr():
    return bar_daily(df2019av,df2020av, gettext("avisdeces.fr"))

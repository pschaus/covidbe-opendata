import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import urllib.request, json


start = '03-10'
end = '04-08'


def necro_count_per_day(df,year):
    necro_count = df.groupby(['Date'])['Date'].agg(['count'])
    necro_count.reset_index(level=0, inplace=True)

    basedate = pd.Timestamp(f'{year}-{start}')
    necro_count['days'] = necro_count.apply(lambda x: (pd.to_datetime(x.Date) - basedate).days, axis=1)

    mask = (necro_count['Date'] >= f'{year}-{start}') & (necro_count['Date'] <= f'{year}-{end}')
    necro_count = necro_count.loc[mask]
    return necro_count


def get_df_im(year):
    necro = pd.read_csv(f'static/csv/inmemoriam_{year}.csv')
    return necro_count_per_day(necro,year)


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

df2019av = get_df_avisdecesfr('2019')
df2020av = get_df_avisdecesfr('2020')




def plot(df2019,df2020,website):
    fig = go.Figure(data=[go.Scatter(x=df2019.days, y=df2019['count'].cumsum(), name='2019'),
                      go.Scatter(x=df2020.days, y=df2020['count'].cumsum(), name='2020'),
                     ])
    fig.update_layout(xaxis_title='#Days',
                      yaxis_title='#Deaths',
                      xaxis = dict(tickmode = 'array', tickvals = df2019['days'], ticktext = df2019['date']),
                      title=f"Cumulated Deaths on {website}", height=500, )

    return fig

def inmemoriam_plot():
    return plot(df2019im,"inmemoriam.be")


def sudpresse_plot():
    return plot(df2019sp, "necro.sudpresse.be")


def sudpresse_plot():
    return plot(df2019av, "avicedes.fr")

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import urllib.request, json


def get_df(year):
    necro = pd.read_csv(f'static/csv/inmemoriam_{year}.csv')
    necro_count = necro.groupby(['Date'])['Date'].agg(['count'])
    necro_count.reset_index(level=0, inplace=True)

    basedate = pd.Timestamp(f'{year}-03-10')
    necro_count['days'] = necro_count.apply(lambda x: (pd.to_datetime(x.Date) - basedate).days, axis=1)

    mask = (necro_count['Date'] >= f'{year}-03-10') & (necro_count['Date'] <= f'{year}-04-08')
    necro_count = necro_count.loc[mask]
    return necro_count


df2019 = get_df('2019')
df2020 = get_df('2020')


def inmemoriam_plot():
    fig = go.Figure(data=[go.Scatter(x=df2019.days, y=df2019['count'].cumsum(), name='2019'),
                      go.Scatter(x=df2020.days, y=df2020['count'].cumsum(), name='2020'),
                     ])
    fig.update_layout(xaxis_title='#Days',
                  yaxis_title='#Deaths',
                  xaxis = dict(tickmode = 'array',tickvals = df2020['days'],ticktext = df2020['Date']),
                  title="Cumulated Deaths since March 10 on inmemoriam.be",height=500,)

    return fig
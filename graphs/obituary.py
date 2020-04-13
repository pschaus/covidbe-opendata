import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import urllib.request, json

from graphs import register_plot_for_embedding

start = '03-10'
end = '04-08'

@register_plot_for_embedding("obituary_inmemoriam")
def get_df_im(year):
    necro = pd.read_csv(f'static/csv/inmemoriam_{year}.csv')
    necro_count = necro.groupby(['Date'])['Date'].agg(['count'])
    necro_count.reset_index(level=0, inplace=True)

    basedate = pd.Timestamp(f'{year}-{start}')
    necro_count['days'] = necro_count.apply(lambda x: (pd.to_datetime(x.Date) - basedate).days, axis=1)

    mask = (necro_count['Date'] >= f'{year}-{start}') & (necro_count['Date'] <= f'{year}-{end}')
    necro_count = necro_count.loc[mask]
    return necro_count

df2019im = get_df_im('2019')
df2020im = get_df_im('2020')


@register_plot_for_embedding("obituary_sudpresse")
def get_df_sudpresse(year):
    necro = pd.read_csv(f'static/csv/necrosudpresse.csv')

    necro_count = necro.groupby(['date'])['date'].agg(['count'])
    necro_count.reset_index(level=0, inplace=True)

    basedate = pd.Timestamp(f'{year}-{start}')
    necro_count['days'] = necro_count.apply(lambda x: (pd.to_datetime(x.date) - basedate).days, axis=1)

    mask = (necro_count['date'] >= f'{year}-{start}') & (necro_count['date'] <= f'{year}-{end}')
    necro_count = necro_count.loc[mask]
    return necro_count


df2019sp = get_df_sudpresse(2019)
df2020sp = get_df_sudpresse(2020)




def inmemoriam_plot():
    fig = go.Figure(data=[go.Scatter(x=df2019im.days, y=df2019im['count'].cumsum(), name='2019'),
                      go.Scatter(x=df2020im.days, y=df2020im['count'].cumsum(), name='2020'),
                     ])
    fig.update_layout(xaxis_title='#Days',
                      yaxis_title='#Deaths',
                      xaxis = dict(tickmode = 'array', tickvals = df2020im['days'], ticktext = df2020im['Date']),
                      title="Cumulated Deaths on inmemoriam.be", height=500, )

    return fig




def sudpresse_plot():

    fig = go.Figure(data=[go.Scatter(x=df2019sp.days, y=df2019sp['count'].cumsum(), name='2019'),
                      go.Scatter(x=df2020sp.days, y=df2020sp['count'].cumsum(), name='2020'),
                     ])
    fig.update_layout(xaxis_title='#Days',
                  yaxis_title='#Deaths',
                  xaxis = dict(tickmode = 'array',tickvals = df2020sp['days'],ticktext = df2020sp['date']),
                  title=f"Cumulated Deaths on necro.sudpresse.be",height=500,)


    return fig



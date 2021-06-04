import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import io
import requests
from zipfile import ZipFile
import pandas
import requests

from graphs import register_plot_for_embedding




df = pd.read_csv('static/csv/international_hospi.csv',parse_dates=['date'])


population = {'United Kingdom':66.65,'France':66.99,'Belgium':11.46,'Netherlands':17.28,'Hungary':9.773,
              'Italy':60.36,'Poland':37.9, 'Portugal':10.28, 'Czechia': 10.69, 'Romania':19.190, 'Spain':47.431 }

df = df.loc[(df['country'] =='Belgium') |
            (df['country'] =='France') |
            (df['country'] =='Netherlands')  |
            (df['country'] =='United Kingdom')|
            (df['country'] =='Hungary')|
            (df['country'] =='Italy')|
            (df['country'] =='Portugal') |
            (df['country'] =='Czechia') | (df['country'] =='Romania') | (df['country'] =='Spain')]

df["pop"] = df["country"].map(lambda x:population[x])
df = df[df.date >= "2020-09-01"]
df['value_per100k'] = df['value']/(df['pop']*10)


@register_plot_for_embedding("hospi_international")
def hospi_international():
    fig = px.line(df[df.indicator =='Daily hospital occupancy'],x="date", y="value_per100k",color="country", title='Hospitals')
    fig.update_layout(template="plotly_white")
    fig.update_layout(yaxis_title="#Hospitalizations/100K")
    return fig

@register_plot_for_embedding("icu_international")
def icu_international():
    fig = px.line(df[df.indicator =='Daily ICU occupancy'], x="date", y="value_per100k",color="country", title='ICU',labels={"date","ICU/100K","ICU/100K"},)
    fig.update_layout(template="plotly_white")
    fig.update_layout(yaxis_title="#ICU/100K")
    return fig




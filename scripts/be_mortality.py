import csv
import requests
import urllib
import pandas as pd
import numpy as np



from datetime import date
from datetime import datetime
from datetime import timedelta
import urllib.request, json

from io import BytesIO
from zipfile import ZipFile
import pandas
import requests

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
import plotly.express as px

import numpy as np
import altair as alt

from datetime import datetime

import geopandas


url = "https://statbel.fgov.be/sites/default/files/files/opendata/deathday/DEMO_DEATH_OPEN.zip"
user_agent = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}
content = requests.get(url,headers = user_agent)
zf = ZipFile(BytesIO(content.content))


# find the first matching csv file in the zip:
match = [s for s in zf.namelist() if ".txt" in s][0]
# the first line of the file contains a string - that line shall de     ignored, hence skiprows

mydateparser = lambda x: datetime.strptime(x, "%d-%m-%Y")


df = pandas.read_csv(zf.open(match), parse_dates=['DT_DATE'],date_parser=mydateparser, low_memory=False,sep="|",encoding="latin-1")


df = df[df['DT_DATE'] >= '2015-01-01']

df.to_csv("../static/csv/mortality_statbel.csv",index=False)


def yearly_mortality_nis3():
    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
    df = pd.read_csv("../static/csv/mortality_statbel.csv", parse_dates=['DT_DATE'], date_parser=dateparse)
    df.dropna(thresh=1, inplace=True)
    df['NIS3'] = df.apply(lambda x: int(str(x['CD_ARR'])[:2]), axis=1).astype(int)
    # df['NIS3'] = df.apply(lambda x: int(str(x['CD_ARR'])[:2]), axis=1).astype(int)
    df['WEEK'] = df.apply(lambda x: x['DT_DATE'].isocalendar()[1], axis=1)
    df = df.groupby(['NR_YEAR', 'NIS3'])["MS_NUM_DEATH"].sum().reset_index()
    df.rename(columns={"MS_NUM_DEATH": "TOT", "NR_YEAR": "YEAR"}, inplace=True)

    geojson = geopandas.read_file('../static/json/admin-units/be-geojson.geojson')
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))
    df = pd.merge(df, df_names, left_on='NIS3', right_on='NIS3', how='left')
    df_pop = pd.read_csv("../static/csv/ins_pop.csv")
    df_pop = df_pop.loc[(df_pop.NIS5 >= 10000) & (df_pop.NIS5 % 1000 == 0) & (df_pop.NIS5 % 10000 != 0)]
    df_pop['NIS3'] = df_pop.NIS5.apply(lambda x: x // 1000)

    df3 = pd.merge(df, df_pop, left_on='NIS3', right_on='NIS3', how='left')
    df3['DEATH_PER_1000HABITANT'] = df3['TOT'] / df3['POP'] * 1000
    df3 = df3.round({'DEATH_PER_1000HABITANT': 2})
    df3 = df3.sort_values(by=['YEAR'])
    df3.to_csv("../static/csv/yearly_mortality_statbel_ins3.csv", index=False)


yearly_mortality_nis3()


def weekly_mortality_all():
    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
    df = pandas.read_csv("../static/csv/mortality_statbel.csv",parse_dates=['DT_DATE'], date_parser=dateparse)

    df = df[df['DT_DATE'] >= '2015-01-01']

    df.dropna(thresh=1,inplace=True)

    def week(date):
        return date.isocalendar()[1]

    df['week'] = df.apply(lambda x: week(x['DT_DATE']), axis=1)


    df_week85 = df.groupby(['NR_YEAR', 'week', 'CD_AGEGROUP'])["MS_NUM_DEATH"].sum().reset_index()
    df_week85.rename(columns={"MS_NUM_DEATH": "tot", "NR_YEAR": "year", "CD_AGEGROUP": "age"}, inplace=True)
    df_week85 = df_week85.loc[(df_week85['age'] == '85+')]
    df_week85.to_csv("../static/csv/weekly_mortality_85+.csv", index=False)


    df_week_all = df.groupby(['NR_YEAR', 'week'])["MS_NUM_DEATH"].sum().reset_index()
    df_week_all.rename(columns={"MS_NUM_DEATH": "tot", "NR_YEAR": "year"}, inplace=True)

    df_week_all.to_csv("../static/csv/weekly_mortality_all.csv", index=False)



weekly_mortality_all()
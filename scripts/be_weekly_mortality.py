import csv
import requests
import urllib
import pandas as pd
import numpy as np



from datetime import date
from datetime import timedelta
from datetime import datetime
import urllib.request, json



DOWNLOAD_URL = "https://epistat.wiv-isp.be/data/Belgium_DailyepistatPub_Riskfactors.csv"
DOWNLOAD_PATH ="../static/csv/be-mortality.csv"

urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)

mydateparser = lambda x: datetime.strptime(x, "%Y%m%d")
df = pd.read_csv(DOWNLOAD_PATH,usecols=["date", "observed"], parse_dates=['date'],date_parser=mydateparser,dtype={"observed":'string'})


def week(date):
    return date.isocalendar()[1]

df['week'] = df.apply(lambda x: week(x['date']), axis=1)

df['year'] = df.apply(lambda x: x['date'].year, axis=1)

df = df[df['year'] >= 2018]

df['observed'].replace('', np.nan, inplace=True)


#todo, dropline with missing values
df = df[df['date'] <= datetime.today() - timedelta(days=20)]


df = df.astype({"observed": int})


df_week = df.groupby(['year','week'])["observed"].sum().reset_index()
df_week.rename(columns={"observed": "tot"},inplace=True)

df_week.to_csv("../static/csv/eu_weekly_mortality/be.csv",index=False)







# mortality belgium

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




url = "https://statbel.fgov.be/sites/default/files/files/opendata/deathday/DEMO_DEATH_OPEN.zip"
content = requests.get(url)
zf = ZipFile(BytesIO(content.content))



# find the first matching csv file in the zip:
match = [s for s in zf.namelist() if ".txt" in s][0]
# the first line of the file contains a string - that line shall de     ignored, hence skiprows

mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y")



df = pandas.read_csv(zf.open(match), parse_dates=['DT_DATE'],date_parser=mydateparser, low_memory=False,sep=";",encoding="latin-1")
df.dropna(thresh=1,inplace=True)

def week(date):
    return date.isocalendar()[1]



df = df[df['DT_DATE'] >= '2018-01-01']


df['week'] = df.apply(lambda x: week(x['DT_DATE']), axis=1)
df_week = df.groupby(['NR_YEAR','week'])["MS_NUM_DEATH"].sum().reset_index()
df_week.rename(columns={"MS_NUM_DEATH": "tot","NR_YEAR": "year"},inplace=True)


df_week.to_csv("../static/csv/eu_weekly_mortality/be.csv",index=False)




# mortality belgium

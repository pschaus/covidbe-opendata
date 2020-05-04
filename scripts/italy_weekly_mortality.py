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

def doit():
    url = "https://www.istat.it/it/files//2020/03/weekly-municipality-deaths.zip"
    content = requests.get(url)
    zf = ZipFile(BytesIO(content.content))

    # find the first matching csv file in the zip:
    match = [s for s in zf.namelist() if ".xlsx" in s][0]


    df = pandas.read_excel(zf.open(match))


    df_week = df.groupby(['WEEK'])['TOTAL_2018','TOTAL_2019','TOTAL_2020'].agg(sum).reset_index()

    def transform(x):
        week = str(x['WEEK'])
        d = date(2020, int(week[3:5]), int(week[0:2]))
        return d.isocalendar()[1]

    df_week['week'] = df_week.apply(transform,axis=1)
    df_week.set_index(['week'],inplace=True)
    df_week = df_week.sort_values(by=['week'])

#doit()
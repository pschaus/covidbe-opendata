import json


import urllib.request, json
import datetime


import pandas as pd
import numpy as np


days = pd.date_range(start='1/1/2020', end=datetime.datetime.now().date())
zeros = np.zeros(len(days))
df = pd.DataFrame({'DATE':days},index=days,)
df.index = pd.to_datetime(df.index)


import urllib.request, json


with open('../static/json/communes/be-centers.json') as json_file:
    centers = json.load(json_file)

for k in centers.keys():
    df[k] = zeros




with urllib.request.urlopen("https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.json") as url:
        data = json.loads(url.read().decode('latin-1'))
        # some entries have no NIS5 or DATE
        data = list(filter(lambda x: "NIS5" in x and "DATE" in x, data))
        for entry in data:
            NIS5 = entry['NIS5']
            ncases = entry['CASES']
            date = datetime.datetime.strptime(entry['DATE'],'%Y-%m-%d').date()
            if ncases == "<5":
                df.at[date,NIS5] = 4
            else:
                df.at[date,NIS5] = int(ncases)


df.to_csv('../static/csv/be-covid-timeseries.csv',index=False)





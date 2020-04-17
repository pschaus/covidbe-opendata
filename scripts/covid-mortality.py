import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests


url="https://epistat.sciensano.be/Data/COVID19BE_MORT.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1')), keep_default_na=False)

df.DATE = pd.to_datetime(df.DATE)

df.to_csv('../static/csv/be-covid-mortality.csv',index=True)
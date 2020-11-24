import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests



url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf8'))) # last line is NaN
df.to_csv('../static/csv/owid.csv',index=False)





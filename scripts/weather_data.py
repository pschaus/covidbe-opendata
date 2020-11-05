import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests

url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf8'))) # last line is NaN

countries = ['BEL','FRA','SWE','ESP','HUN','AUT','DEU']
df = df[df['iso_code'].isin(countries)]

print(df)


#df.to_csv('../static/csv/weather.csv',index=False)





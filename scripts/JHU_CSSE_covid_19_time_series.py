import urllib.request, json
import pandas as pd
import numpy as np
import io
import requests


url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1')))
df.to_csv('../static/csv/time_series_covid19_confirmed_global.csv', index=False)

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1')))
df.to_csv('../static/csv/time_series_covid19_deaths_global.csv', index=False)

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1')))
df.to_csv('../static/csv/time_series_covid19_recovered_global.csv', index=False)
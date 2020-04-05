import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests



prov_codes = {"VlaamsBrabant": "VBR",
              "Namur": "WNA",
              "Hainaut": "WHT",
              "OostVlaanderen": "VOV",
              "Brussels": "BRU",
              "WestVlaanderen": "VWV",
              "Limburg": "VLI",
              "Antwerpen": "VAN",
              "Liège": "WLG",
              "Luxembourg": "WLX",
              "BrabantWallon": "WBR"}


url="https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1')),skipfooter=1) # last line is NaN

df['PROVINCE']= df['PROVINCE'].map(prov_codes)


df_tot_provinces = df.groupby('PROVINCE').agg({'CASES': 'sum'})


df_tot_provinces.to_csv('../static/csv/be-covid-provinces_tot.csv',index=True)



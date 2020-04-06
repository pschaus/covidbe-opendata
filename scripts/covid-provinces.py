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

prov_population = {"VBR":1129849,
              "WNA":491285,
              "WHT":1339562,
              "VOV":1186532,
              "BRU":1191604,
              "VWV":1496187,
              "VLI":867413,
              "VAN":1836030,
              "WLG":1102531,
              "WLX":281972,
              "WBR":399123}



url="https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('latin-1'))) # last line is NaN

# MAP PROVINCE CODES
df['PROVINCE']= df['PROVINCE'].map(prov_codes)

# Filter NaN (yes the data is not totally clean)
df.dropna(inplace=True)
df.DATE = pd.to_datetime(df.DATE)

df.to_csv('../static/csv/be-covid-provinces.csv',index=True)


# total number per provinces
df_tot_provinces = df.groupby('PROVINCE').agg({'CASES': 'sum'})
df_tot_provinces["POPULATION"] = df_tot_provinces.index.map(mapper=prov_population)
df_tot_provinces["CASES_PER_THOUSAND"] = df_tot_provinces["CASES"]*1000/df_tot_provinces["POPULATION"]
df_tot_provinces.to_csv('../static/csv/be-covid-provinces_tot.csv',index=True)










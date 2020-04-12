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

prov_codes_ = {v:k for k,v in prov_codes.items()}

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
df_prov=pd.read_csv(io.StringIO(s.decode('latin-1'))) # last line is NaN

# MAP PROVINCE CODES
df_prov['PROVINCE_NAME']= df_prov['PROVINCE']
df_prov['PROVINCE']= df_prov['PROVINCE'].map(prov_codes)

# Filter NaN (yes the data is not totally clean)
df_prov.dropna(inplace=True)
df_prov.DATE = pd.to_datetime(df_prov.DATE)

df_prov.to_csv('../static/csv/be-covid-provinces.csv', index=True)


# ----------------------------------------------------



url="https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv"
s=requests.get(url).content
df_hospi=pd.read_csv(io.StringIO(s.decode('latin-1'))) # last line is NaN

# MAP PROVINCE CODES
df_hospi['PROVINCE_NAME']= df_hospi['PROVINCE']
df_hospi['PROVINCE']= df_hospi['PROVINCE'].map(prov_codes)


# Filter NaN (yes the data is not totally clean)
df_hospi.dropna(inplace=True)
df_hospi.DATE = pd.to_datetime(df_hospi.DATE)

df_hospi.to_csv('../static/csv/be-covid-hospi.csv', index=True)


# -----------------------------------------------------------------


# total number of cases per provinces
df_tot_provinces = df_prov.groupby(['PROVINCE']).agg({'CASES': 'sum'})


df_tot_provinces['PROVINCE_NAME'] = df_tot_provinces.index.map(prov_codes_)

df_tot_provinces["POPULATION"] = df_tot_provinces.index.map(mapper=prov_population)
df_tot_provinces["CASES_PER_THOUSAND"] = df_tot_provinces["CASES"]*1000/df_tot_provinces["POPULATION"]

df_tot_provinces_hospi = df_hospi.groupby('PROVINCE').agg({'NEW_IN': 'sum'})

df_tot_provinces["NEW_IN"] = df_tot_provinces_hospi['NEW_IN']

df_tot_provinces["NEW_IN_PER_CASES"] = df_tot_provinces_hospi['NEW_IN']/df_tot_provinces["CASES"] #nombre d'hospi/nombre de cas
df_tot_provinces.to_csv('../static/csv/be-covid-provinces_tot.csv',index=True)

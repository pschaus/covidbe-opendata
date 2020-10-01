import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests


url="https://epistat.sciensano.be/Data/COVID19BE_tests.csv"
s=requests.get(url).content
df_testing=pd.read_csv(io.StringIO(s.decode('latin-1')),index_col = 0) # last line is NaN

df_testing = df_testing.groupby(['DATE']).agg({'TESTS_ALL': 'sum','TESTS_ALL_POS': 'sum'})

#df_testing.index = pd.to_datetime(df_testing.index)



url="https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv"
s=requests.get(url).content
df_prov=pd.read_csv(io.StringIO(s.decode('latin-1'))) # last line is NaN


# total number of cases per provinces
df_totcase = df_prov.groupby(['DATE']).agg({'CASES': 'sum'})



df_testing['CASES']=df_totcase.CASES


df_testing.to_csv('../static/csv/be-covid-testing.csv',index=True)





import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests


url="https://epistat.sciensano.be/Data/COVID19BE_VACC.csv"
s=requests.get(url).content
df_vaccines=pd.read_csv(io.StringIO(s.decode('latin-1')),index_col = 0) # last line is NaN

df_vaccines.to_csv('../static/csv/be-covid-vaccines.csv',index=True)





import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests





url="https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/csv/data.csv"
s=requests.get(url).content
df_hospi=pd.read_csv(io.StringIO(s.decode('utf8'))) # last line is NaN
df_hospi.to_csv('../static/csv/international_hospi.csv',index=False)





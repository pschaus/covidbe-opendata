import csv
import requests
import urllib
import pandas as pd

DOWNLOAD_URL = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
DOWNLOAD_PATH ="../static/csv/google_mobility_report.csv"
urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)

df = pd.read_csv(DOWNLOAD_PATH)

df_eu = df[df['country_region_code'].isin(['BE', 'FR','NL','DE','LU','GB','PT','SP','IT','SE','PL'])]
df_eu = df_eu[df_eu['sub_region_1'].isnull()]
df_eu.to_csv("../static/csv/google_mobility_report_eu.csv",index=False)



df_be = df[df['country_region_code'].isin(['BE'])]
df_be.to_csv("../static/csv/google_mobility_report_be.csv",index=False)


df_cities = df[df['sub_region_1'].isin(['Île-de-France', 'Brussels','Greater London','Berlin','North Holland'])]
df_cities.to_csv("../static/csv/google_mobility_report_cities.csv",index=False)


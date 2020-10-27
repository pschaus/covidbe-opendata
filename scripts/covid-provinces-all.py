import pandas as pd
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

prov_population = {"VBR":1155843,
              "WNA":495832,
              "WHT":1346840,
              "VOV":1200945,
              "BRU":1218255,
              "VWV":1525255,
              "VLI":877370,
              "VAN":1869730,
              "WLG":1109800,
              "WLX":286752,
              "WBR":406019}

url="https://epistat.sciensano.be/Data/COVID19BE_tests.csv"
s=requests.get(url).content
df_testing_prov=pd.read_csv(io.StringIO(s.decode('utf8')),index_col = 0) # last line is NaN


url="https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv"
s=requests.get(url).content
df_case_prov=pd.read_csv(io.StringIO(s.decode('utf8'))) # last line is NaN


df_case_prov['PROVINCE_NAME']= df_case_prov['PROVINCE']
df_case_prov = df_case_prov.groupby(['DATE','PROVINCE_NAME']).agg({'CASES': 'sum'}).reset_index()


df = df_case_prov.merge(df_testing_prov, how='left', left_on=['DATE','PROVINCE_NAME'],right_on=['DATE','PROVINCE'])


url="https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv"
s=requests.get(url).content
df_hospi=pd.read_csv(io.StringIO(s.decode('utf8'))) # last line is NaN
df = df[['DATE', 'PROVINCE','TESTS_ALL','TESTS_ALL_POS','CASES']]
df = df[df['DATE'] >= '2020-03-15']
df = df.merge(df_hospi, how='right', on=['DATE','PROVINCE'])
df['PROV']= df['PROVINCE'].map(prov_codes)
df['POP']= df['PROV'].map(prov_population)

df.to_csv('../static/csv/be-covid-provinces-all.csv', index=False)
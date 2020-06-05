import urllib.request
import json
import pandas as pd
import geopandas




DOWNLOAD_URL = "https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv"
DOWNLOAD_PATH ="../static/csv/COVID19BE_CASES_MUNI.csv"
urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)



def covid_weekly_ins5():
    df = pd.read_csv("../static/csv/COVID19BE_CASES_MUNI.csv", parse_dates=['DATE'], encoding='latin1')
    df = df[['DATE', 'NIS5', 'CASES', 'TX_DESCR_FR']]
    df.rename(columns={'TX_DESCR_FR': "name"}, inplace=True)
    df.dropna(inplace=True)
    df['WEEK'] = df.apply(lambda x: x['DATE'].isocalendar()[1], axis=1)
    df = df.replace({'<5': '1'})
    df['CASES'] = df['CASES'].astype(int)
    df['NIS5'] = df['NIS5'].astype(int)

    df5 = df.groupby([df.NIS5, df.WEEK, df.name]).agg({'CASES': ['sum']}).reset_index()
    df5.columns = df5.columns.get_level_values(0)

    df_pop = pd.read_csv("../static/csv/ins_pop.csv", dtype={"NIS5": int})

    df5 = pd.merge(df5, df_pop, left_on='NIS5', right_on='NIS5', how='left')
    df5['CASES_PER_1000HABITANT'] = df5['CASES'] / df5['POP'] * 1000
    df5 = df5.round({'CASES_PER_1000HABITANT': 2})
    df5 = df5.sort_values(by=['WEEK'])
    df5.to_csv("../static/csv/cases_weekly_ins5.csv")



def covid_weekly_ins3():
    df = pd.read_csv("../static/csv/COVID19BE_CASES_MUNI.csv", parse_dates=['DATE'], encoding='latin1')
    df = df[['DATE', 'NIS5', 'CASES']]

    df.dropna(inplace=True)
    df['NIS5'] = df['NIS5'].astype(int).astype(str)
    df['NIS3'] = df.apply(lambda x: x['NIS5'][:2], axis=1).astype(int)

    def week(date):
        return date.isocalendar()[1]

    df['WEEK'] = df.apply(lambda x: week(x['DATE']), axis=1)

    df = df.replace({'<5': '1'})
    df['CASES'] = df['CASES'].astype(int)

    df3 = df.groupby([df.NIS3, df.WEEK]).agg({'CASES': ['sum']}).reset_index()
    df3.columns = df3.columns.get_level_values(0)

    geojson = geopandas.read_file('../static/json/admin-units/be-geojson.geojson')
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))
    df3 = pd.merge(df3, df_names, left_on='NIS3', right_on='NIS3', how='left')

    df_pop = pd.read_csv("../static/csv/ins_pop.csv", dtype={"NIS5": int})
    df_pop = df_pop.loc[(df_pop.NIS5 >= 10000) & (df_pop.NIS5 % 1000 == 0) & (df_pop.NIS5 % 10000 != 0)]
    df_pop['NIS3'] = df_pop.NIS5.apply(lambda x: x//1000)

    df3 = pd.merge(df3, df_pop, left_on='NIS3', right_on='NIS3', how='left')
    df3['CASES_PER_1000HABITANT'] = df3['CASES'] / df3['POP'] * 1000
    df3 = df3.round({'CASES_PER_1000HABITANT': 2})
    df3 = df3.sort_values(by=['WEEK'])
    df3.to_csv("../static/csv/cases_weekly_ins3.csv")

covid_weekly_ins5()
covid_weekly_ins3()

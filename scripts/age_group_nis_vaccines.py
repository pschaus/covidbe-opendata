#https://statbel.fgov.be/fr/open-data/population-par-lieu-de-residence-nationalite-etat-civil-age-et-sexe-10

import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests

def df_pop():
    df_pop =pd.read_csv("static/csv/TF_SOC_POP_STRUCT_2020.csv",sep=";",encoding='latin') # last line is NaN

    df_pop = df_pop.groupby(by=['CD_REFNIS', 'TX_DESCR_FR', 'CD_AGE']).agg({'MS_POPULATION': ['sum']}).reset_index()
    df_pop.columns = df_pop.columns.get_level_values(0)

    print(df_pop[df_pop.CD_REFNIS  == 11001][0:100])

    bins= [12,16,18,25,35,45,55,65,75,85,120]
    labels = ['12-15','16-17','18-24','25-34','35-44','45-54','55-64','65-74','75-84','85+']
    df_pop['AgeGroup'] = pd.cut(df_pop['CD_AGE'], bins=bins, labels=labels, right=False)

    df_pop = df_pop.groupby(by=['CD_REFNIS','AgeGroup']).agg({'MS_POPULATION': ['sum']}).reset_index()

    df_pop.columns = df_pop.columns.get_level_values(0)

    df_pop = df_pop.rename(columns = {'CD_REFNIS': 'NIS5', 'MS_POPULATION': 'COUNT'}, inplace = False)

    df_pop.to_csv('static/csv/pop-age-group-nis5.csv',index=False)



#https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv

#static/csv/TF_SOC_POP_STRUCT_2020.csv


import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests

def vaccines_pop():
    url="https://epistat.sciensano.be/data/COVID19BE_VACC_MUNI_CUM.csv"
    s=requests.get(url).content
    df_vaccines=pd.read_csv(io.StringIO(s.decode('latin-1'))) # last line is NaN

    df_vaccines.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    df_vaccines['NIS5'] = df_vaccines['NIS5'].astype(int).astype(str)


    df_vaccines.to_csv('../static/csv/be-covid-vaccines-nis.csv')


    df_vaccines["CUMUL"].replace({"<10": "0"}, inplace=True)
    df_vaccines['CUMUL'] = df_vaccines['CUMUL'].astype(int)




    df_pop =pd.read_csv("../static/csv/pop-age-group-nis5.csv",sep=",",encoding='latin') # last line is NaN
    df_pop['NIS5'] = df_pop['NIS5'].astype(str)
    df_pop['COUNT'] = df_pop['COUNT'].astype(int)



    last_week = df_vaccines.YEAR_WEEK.values[-1]

    df_vaccines = df_vaccines[df_vaccines.YEAR_WEEK == last_week]

    df_vaccines = df_vaccines[df_vaccines.DOSE != 'B']



    df_vaccines = df_vaccines.groupby(by=['YEAR_WEEK', 'NIS5', 'AGEGROUP']).agg({'CUMUL': ['sum']}).reset_index()
    df_vaccines.columns = df_vaccines.columns.get_level_values(0)




    df = pd.merge(df_vaccines, df_pop, left_on=['NIS5','AGEGROUP'], right_on=['NIS5','AgeGroup'])

    print(df[:100])


    df['percent'] = 100*df['CUMUL']/df['COUNT']

    df.to_csv('../static/csv/vaccines_age_group_nis5.csv', index=False)


def df_vaccine_nis_percentage():
    df_vaccines = pd.read_csv('../static/csv/be-covid-vaccines-nis.csv', dtype={"NIS5": int})

    df_vaccines["CUMUL"].replace({"<10": "0"}, inplace=True)
    df_vaccines['CUMUL'] = df_vaccines['CUMUL'].astype(int)

    last_week = df_vaccines.YEAR_WEEK.values[-1]

    df_vaccines = df_vaccines[df_vaccines.YEAR_WEEK == last_week]

    df_vaccines = df_vaccines[df_vaccines.DOSE != 'B']

    df_vaccines = df_vaccines.groupby(by=['YEAR_WEEK', 'NIS5']).agg({'CUMUL': ['sum']}).reset_index()
    df_vaccines.columns = df_vaccines.columns.get_level_values(0)

    df_pop = pd.read_csv("../static/csv/ins_pop.csv", dtype={"NIS5": int})
    df_pop = df_pop.loc[(df_pop.NIS5 >= 10000)]

    df5 = pd.merge(df_vaccines, df_pop, left_on='NIS5', right_on='NIS5', how='inner')
    df5['PERCENT'] = df5['CUMUL'] / df5['POP'] * 100
    df5 = df5.round({'PERCENT': 2})

    df5.to_csv("../static/csv/vaccines_ins5_percentage.csv")

vaccines_pop()
df_vaccine_nis_percentage()
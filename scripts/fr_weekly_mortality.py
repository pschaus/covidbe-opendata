# import csv
# import requests
# import urllib
# import pandas as pd
# import numpy as np
#
#
#
# from datetime import date
# from datetime import datetime
# from datetime import timedelta
# import urllib.request, json
#
# from io import BytesIO
# from zipfile import ZipFile
# import pandas
# import requests
#
# url = "https://www.insee.fr/fr/statistiques/fichier/4470857/2020-04-24_deces_quotidiens_departement_csv.zip"
# content = requests.get(url)
# zf = ZipFile(BytesIO(content.content))
#
# for item in zf.namelist():
#     print("File in zip: "+  item)
#
# # find the first matching csv file in the zip:
# match = [s for s in zf.namelist() if ".csv" in s][0]
# # the first line of the file contains a string - that line shall de     ignored, hence skiprows
#
# mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y")
#
#
# df = pandas.read_csv(zf.open(match), parse_dates=['Date_evenement'],date_parser=mydateparser, low_memory=False,sep=";")
# df = df[df.Zone=="France"]
# df.dropna(thresh=1,inplace=True)
#
# def week(date):
#     return date.isocalendar()[1]
#
#
#
#
# df['week'] = df.apply(lambda x: week(x['Date_evenement']), axis=1)
#
#
# df = df.loc[:, ['week', 'Total_deces_2020','Total_deces_2019','Total_deces_2018']]
#
#
# def aggr_week(series):
#     return series.max()-series.min()
#
# df_week = df.groupby(['week'])['Total_deces_2020','Total_deces_2019','Total_deces_2018'].agg(aggr_week).reset_index()#.sum().reset_index()
#
# df2018 = df_week.loc[:, ['week','Total_deces_2018']]
# df2018["year"]=2018
# df2018.rename(columns={'Total_deces_2018': "tot"},inplace=True)
#
#
#
# df2019 = df_week.loc[:, ['week','Total_deces_2019']]
# df2019["year"]=2019
# df2019.rename(columns={'Total_deces_2019': "tot"},inplace=True)
#
# df2020 = df_week.loc[:, ['week','Total_deces_2020']]
# df2020["year"]=2020
# df2020.rename(columns={'Total_deces_2020': "tot"},inplace=True)
#
# df = df2018.append(df2019).append(df2020)
#
# df.to_csv("../static/csv/eu_weekly_mortality/fr.csv",index=False)
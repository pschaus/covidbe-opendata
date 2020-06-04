import pandas as pd
import os

def process_population():
    path = '../static/csv/facebook/hidden/population/'
    df_all = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.read_csv(entry.path)
        df = df.loc[df.country == 'BE']
        df_all = pd.concat([df_all,df])

    if df_all.empty:
        return

    df_all.drop(['spaco_id','country','level','lat','lon'],axis=1,inplace=True)
    df_all.rename(columns={'polygon_name':'name'},inplace=True)
    df_all.date_time = pd.to_datetime(df_all.date_time, format='%Y-%m-%d %H%M')
    df_all = df_all.groupby(['name', pd.Grouper(key='date_time', freq='D')]).agg({
               'n_baseline':'sum',
               'n_crisis':'sum',
           }).reset_index()
    df_all['percent_change'] = (df_all.n_crisis - df_all.n_baseline) / df_all.n_baseline
    df_all.sort_values(by=['date_time'],inplace=True)

    df_all.to_csv("../static/csv/facebook/population.csv",index=False)

def process_movement_range():
    path = '../static/csv/facebook/hidden/movement-range/'
    df_all = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.read_csv(entry.path)
        df_all = pd.concat([df_all,df])

    if df_all.empty:
        return

    df_all.drop(['crisis_name','polygon_id','age_bracket','gender','baseline_name','baseline_type','external_polygon_id_type','external_polygon_id'],axis=1,inplace=True)
    df_all = df_all.loc[:, ~df_all.columns.str.contains('^Unnamed')]
    df_all.rename(columns={'ds':'date_time'}, inplace=True)
    df_all = df_all.sort_values(by=['date_time'])

    df_all.to_csv("../static/csv/facebook/movement-range.csv",index=False)

process_population()
process_movement_range()

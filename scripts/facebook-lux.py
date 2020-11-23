import pandas as pd
import os

def process_movement():
    path = '../static/csv/facebook/hidden/movement-lux/'
    df_all = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.read_csv(entry.path)
        df_all = pd.concat([df_all,df])

    if df_all.empty:
        return

    #df_all = df_all.loc[df_all.country == 'BE']
    df_all = df_all.drop(
        ['geometry','start_polygon_id','end_polygon_id','length_km','level','tile_size','country',
        'is_statistically_significant','n_difference','percent_change','z_score'],
        axis=1
    )
    #df_all = df_all.loc[~(df_all.start_polygon_name == df_all.end_polygon_name)]
    df_all.rename(columns={'start_polygon_name':'start_name', 'end_polygon_name':'end_name'}, inplace=True)
    df_all = df_all.sort_values(by=['date_time'])

    df_all.to_csv("../static/csv/facebook/movement-lux.csv",index=False)

process_movement()


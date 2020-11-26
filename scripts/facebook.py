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
    df_all.rename(columns={'ds':'date_time', 'polygon_name':'name'}, inplace=True)
    df_all = df_all.sort_values(by=['date_time'])

    df_all.to_csv("../static/csv/facebook/movement-range.csv",index=False)

def process_movement():
    path = '../static/csv/facebook/hidden/movement/'
    df_all = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.read_csv(entry.path)
        df_all = pd.concat([df_all,df])

    if df_all.empty:
        return

    df_all = df_all.loc[df_all.country == 'BE']
    df_all = df_all.drop(
        ['geometry','start_polygon_id','end_polygon_id','length_km','level','tile_size','country',
        'is_statistically_significant','n_difference','percent_change','z_score'],
        axis=1
    )
    #df_all = df_all.loc[~(df_all.start_polygon_name == df_all.end_polygon_name)]
    df_all.rename(columns={'start_polygon_name':'start_name', 'end_polygon_name':'end_name'}, inplace=True)
    df_all = df_all.sort_values(by=['date_time'])

    df_all.to_csv("../static/csv/facebook/movement.csv",index=False)

def process_colocation():
    path = '../static/csv/facebook/hidden/colocation/'
    df = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.concat([df,pd.read_csv(entry.path)])

    if df.empty:
        return

    df = df.loc[df.country == 'BEL']
    df = df.drop(['polygon1_id','name_stack_1','polygon2_id','name_stack_2','country','lon_1','lat_1','lon_2','lat_2'], axis=1)
    df.link_value = df.apply(lambda x: 0 if x.polygon1_name == x.polygon2_name else x.link_value, axis=1)

    df.rename(columns={'polygon1_name':'name1', 'polygon2_name':'name2'}, inplace=True)

    df.to_csv("../static/csv/facebook/colocation.csv",index=False)



def process_travel_maps():
    path = '../static/csv/facebook/hidden/travel-maps/'
    df_all = pd.DataFrame()

    for entry in os.scandir(path):
        df = pd.read_csv(entry.path)
        df_all = pd.concat([df_all, df])

    if df_all.empty:
        return

    df_all = df_all.drop(
        ['polygon1_id', 'latitude1', 'longitude1', 'polygon2_id', 'latitude2', 'longitude2', 'metric_name'],
        axis=1
    )

    # df_all = df_all.loc[~(df_all.start_polygon_name == df_all.end_polygon_name)]
    df_all.rename(columns={'polygon1_name': 'start_name', 'polygon2_name': 'end_name', 'metric_value': 'travel_counts'},
                  inplace=True)
    df_all = df_all.sort_values(by=['ds'])
    df_all.to_csv("../static/csv/facebook/movement_countries.csv", index=False)



process_population()
process_movement_range()
process_movement()
process_colocation()
process_travel_maps()
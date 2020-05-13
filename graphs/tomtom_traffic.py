import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

######################################## 1

# importing modules
import pandas as pd
import plotly.express as px
import datetime

# Loading dataset from an url

def get_belgium_df_working_days() :

    belgium = ["antwerp", "brussels", "charleroi", "ghent", "kortrijk", "leuven", "liege", "mons", "namur"]

    belgium_df = pd.DataFrame()

    for e in belgium:
        df = pd.read_csv("static/csv/tomtom/BEL_" + e + ".csv")
        df['city'] = e
        df['Time'] = pd.to_datetime(df['Time'])
        df.index = df['Time']
        df = df.between_time('07:00', '09:00')
        df = df[df.index.dayofweek < 5]
        df = df[df.Time.dt.date != datetime.date(2020, 5, 1)]
        df = df[df.Time.dt.date > datetime.date(2020, 4, 14)]
        df = df.groupby([df.city, df.Time.dt.date]).agg(['mean'])
        df.columns = df.columns.droplevel(1)
        belgium_df = belgium_df.append(df, ignore_index=False)  # Add df one by one
    
    return belgium_df


@register_plot_for_embedding("tomtom_traffic_working_days")
def plot_tomtom_be_working_days():
    """
    tomtom traffic working days
    """
    
    belgium_df = get_belgium_df_working_days()
    
    # Plotting a Map to show real-time traffic around the world
    # fig = px.bar(bel_bru, y='LiveTraffic', x='Time')
    fig = px.line(belgium_df, y='LiveTraffic', x=belgium_df.index.get_level_values(1),
                  color=belgium_df.index.get_level_values(0))

    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide',
                      xaxis_title="TomTom Traffic Index",
                      yaxis_title="Day",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

######################################## 2

# importing extra modules
from os import listdir
from os.path import isfile, join

# Loading dataset from a file

def get_belgium_neighbors_df_working_days() :
    mypath = "static/csv/tomtom/"

    placefiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    placefiles.sort()

    ##print(placefiles)

    places_df = pd.DataFrame()

    selected = placefiles[1:]

    for e in selected :

        df = pd.read_csv(mypath+e)

        keys = e.strip().replace(".","_").strip().split("_")

        df['key'] = keys[0] + '_' + keys[1]
        df['country'] = keys[0].strip()+""
        df['city'] = keys[1].strip()+""

        df['Time'] = pd.to_datetime(df['Time'])
        df['Hour'] = df.Time.dt.hour
        df['Date'] = df.Time.dt.date
        df.index = df['Time']

        df = df.between_time('07:00', '09:00')
        df = df[df.index.dayofweek < 5]
        df = df[df.Time.dt.date != datetime.date(2020,5,1)]
        df = df[df.Time.dt.date > datetime.date(2020,4,13)]

        #df = df.groupby([df.country, df.city,  df.Date, df.Hour]).agg(['mean'])
        df = df.groupby([df.country, df.city,  df.Date]).agg(['mean'])

        df.columns = df.columns.droplevel(1)

        places_df = places_df.append(df, ignore_index=False) # Add df one by one

    # Exploring the dataset

    #placed_df = pd.merge(places_df, world, how='left', on=['country', 'city'], indicator='indicator_column', left_index=False, right_index=False)

    #response = requests.get("https://api.midway.tomtom.com/ranking/live/")

    #world = pd.json_normalize(json.loads(response.text))

    #world[['country','shape','city']] = world["circle.key"].str.split("/", expand = True)
    #world['data.UpdateTime'] = pd.to_datetime(world['data.UpdateTime'], unit = "ms")
    #world.city = world.city.astype(str)
    #world.country = world.country.astype(str)

    #lonlat = world[['country', 'city', 'circle.shape.centerLon','circle.shape.centerLat']]

    #lonlat.to_csv(mypath+"all/citieslonlat.csv", index=False)

    lonlat = pd.read_csv(mypath+"all/citieslonlat.csv")

    #print(lonlat)

    lonlat.set_index(['country', 'city'], inplace=True)
    lonlat = lonlat.reset_index().drop_duplicates(subset=['country', 'city'], keep='last').set_index(['country', 'city'])

    places_df = places_df.join(lonlat)

    places_df['country'] = places_df.index.get_level_values(0)
    places_df['city'] = places_df.index.get_level_values(1)
    #places_df['Hour'] = places_df.index.get_level_values(2)
    places_df['Date'] = places_df.index.get_level_values(2)#(3)

    places_df['DateH'] = pd.to_datetime(places_df['Date'])
    #places_df['DateH'] += pd.to_timedelta(places_df.Hour, unit='h')
    places_df.DateH = places_df.DateH.dt.strftime('%Y-%m-%d')#('%Y-%m-%d %H')

    return places_df


@register_plot_for_embedding("map_tomtom_be_working_days")
def map_tomtom_be_working_days():
    """
    tomtom traffic map working days
    """

    places_df = get_belgium_neighbors_df_working_days()

    fig = px.scatter_mapbox(places_df,
                            lat = "circle.shape.centerLat",
                            lon = "circle.shape.centerLon",
                            color = "LiveTraffic",#"data.JamsDelay",
                            size = "LiveTraffic",
                            color_continuous_scale = px.colors.sequential.Viridis,
                            range_color = [min(places_df.LiveTraffic),max(places_df.LiveTraffic)],
                            animation_frame="DateH",
                            size_max=20,
                            zoom = 7, center = {"lat": 50.8466, "lon": 4.3528})#,
                            #hover_name="city", hover_data=["country", "data.JamsDelay", "data.JamsCount", "data.JamsLength", "data.UpdateTime"])

    fig.update_layout(mapbox_style="carto-positron")


    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

######################################## 3

# Loading dataset from a file

def get_world_df() :
    # Loading dataset from a file
    mypath = "static/csv/tomtom/"
    df = pd.read_csv(mypath + "all/all.csv")

    df[['country', 'shape', 'city']] = df["key"].str.split("/", expand=True)
    df['Time'] = pd.to_datetime(df['UpdateTime'], unit="ms")

    df['Hour'] = df.Time.dt.hour
    df['Min'] = df.Time.dt.minute
    df['Date'] = df.Time.dt.date
    df.index = df['Time']

    print(df.Date.min())

    # df = df.between_time('07:00', '09:00')
    df = df[df.index.dayofweek < 5]
    df = df[df.Time.dt.date != datetime.date(2020, 5, 1)]
    df = df[df.Time.dt.date > datetime.date(2020, 4, 13)]

    df = df.groupby([df.country, df.city, df.Date, df.Hour]).agg(['mean'])
    df.columns = df.columns.droplevel(1)

    # print(df)

    df['country'] = df.index.get_level_values(0)
    df['city'] = df.index.get_level_values(1)
    df['Date'] = df.index.get_level_values(2)
    df['Hours'] = df.index.get_level_values(3)
    #df['Min'] = df.index.get_level_values(4)

    #df['HMin'] = df['Hour'].astype(str) + ':' + df['Min'].astype(str)

    return df

world_df = get_world_df()

@register_plot_for_embedding("map_tomtom_by_day")
def map_tomtom_by_day(date, hour):
    """
    tomtom traffic map by day
    """

    ddate = datetime.datetime.strptime(date, '%Y-%m-%d')
    print("treats", ddate, type(ddate), hour, type(hour))

    world_df_day = world_df[(world_df.Date == ddate.date()) & (world_df.Hours == int(hour))]#.sort_values(by = ['Hours'])

    #datetime.date(2020, 5, 7)
    print(world_df_day.head())

    print("date selected : ", date, type(date))

    fig = px.scatter_mapbox(data_frame=world_df_day,
                            lat="lat",
                            lon="lon",
                            color="LiveTraffic",  # "data.JamsDelay",
                            size="LiveTraffic",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            range_color=[min(world_df.LiveTraffic), max(world_df.LiveTraffic)],
                            #animation_frame="Hours",
                            size_max=20,
                            zoom=7, center={"lat": 50.8466, "lon": 4.3528})  # ,
    # hover_name="city", hover_data=["country", "data.JamsDelay", "data.JamsCount", "data.JamsLength", "data.UpdateTime"])

    fig.update_layout(mapbox_style="carto-positron")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig





import csv
import requests
import pandas as pd
import time
import os
from os import path

def update():
    print("fetch")
    # retrieve json file
    url = "https://api.midway.tomtom.com/ranking/live/"
    italy_req = requests.get(url)
    italy_json = italy_req.json()

    pd.set_option("display.max_rows", False)

    # create empty lists of append data
    keys_city = []
    city_tzon = []
    lats_city = []
    lons_city = []
    
    live_traffic = []
    jams_delay = []
    jams_length = []
    jams_count = []
    
    time = []

    count = len(italy_json) - 1
    print(count)

    # append each item in the json file to the empty lists
    i = 0
    while i <= count:
        # print(italy_json["data"][i])
        keys_city.append(italy_json[i]['circle']['key'])
        city_tzon.append(italy_json[i]['circle']['timezone'])
        lats_city.append(italy_json[i]['circle']['shape']['centerLat'])
        lons_city.append(italy_json[i]['circle']['shape']['centerLon'])
        
        live_traffic.append(italy_json[i]["data"]["TrafficIndexLive"])
        jams_delay.append(italy_json[i]["data"]["JamsDelay"])
        jams_length.append(italy_json[i]["data"]["JamsLength"])
        jams_count.append(italy_json[i]["data"]["JamsCount"])

        time.append(italy_json[i]["data"]["UpdateTime"])
        i += 1

    # create dataframe with the traffic data
    df = pd.DataFrame(
        {"key": keys_city, 
        "timezone": city_tzon, 
        "lat": lats_city, 
        "lon": lons_city, 
        "LiveTraffic": live_traffic, 
        "JamsDelay": jams_delay, 
        "JamsLength": jams_length, 
        "JamsCount": jams_count, 
        "UpdateTime": time},
        index=time)
    df.index = pd.to_datetime(df.index, unit="ms")
    df.index.name = "Time"
    df.head()

    if path.exists("../static/csv/tomtom/all.csv") :
        df_ = pd.read_csv(f"../static/csv/tomtom/all.csv", index_col=0, parse_dates=True)

        df = pd.concat([df,df_])
    
	
    df = df.reset_index().drop_duplicates(subset=['UpdateTime', 'key'], keep='last').set_index('Time')

    df = df.sort_values(by=['Time'])
    df.to_csv(f"../static/csv/tomtom/all.csv")


while True:
	update()
	time.sleep(5*60)






import csv
import requests
import pandas as pd


cities_be = ["BEL_antwerp", "BEL_bruges", "BEL_brussels", "BEL_charleroi", "BEL_liege",
             "BEL_ghent", "BEL_leuven", "BEL_kortrijk", "BEL_mons", "BEL_namur"]

cities = ["CHN_beijing", "CAN_toronto", "USA_los-angeles", "JPN_tokyo", "ARE_abu-dhabi",
          "HKG_hong-kong", "GBR_london", "FRA_bordeaux", "FRA_lyon", "ITA_milan", "CZE_prague",
          "ESP_barcelona", "AUT_vienna", "NOR_oslo", "SWE_stockholm", "USA_chicago",
          "NLD_amsterdam", "ESP_madrid", "FRA_paris", "IRL_dublin", "DEU_berlin", "DNK_copenhagen",
          "ITA_rome", "SWE_stockholm", "PRT_porto", "USA_new-york", "RUS_moscow", "BRA_rio-de-janeiro",
          "AUS_melbourne", "TUR_ankara", "ARE_dubai", "ZAF_johannesburg"]

def update(country):
    print(country)
    # retrieve json file
    url = f"https://api.midway.tomtom.com/ranking/live/{country}"
    italy_req = requests.get(url)
    italy_json = italy_req.json()

    pd.set_option("display.max_rows", False)

    # create empty lists of append data
    live_traffic = []
    jams_delay = []
    jams_length = []
    jams_count = []

    time = []

    count = len(italy_json["data"]) - 1

    # append each item in the json file to the empty lists
    i = 0
    while i <= count:
        # print(italy_json["data"][i])
        live_traffic.append(italy_json["data"][i]["TrafficIndexLive"])
        jams_delay.append(italy_json["data"][i]["JamsDelay"])
        jams_length.append(italy_json["data"][i]["JamsLength"])
        jams_count.append(italy_json["data"][i]["JamsCount"])

        time.append(italy_json["data"][i]["UpdateTime"])
        i += 1

    # create dataframe with the traffic data
    df = pd.DataFrame(
        {"LiveTraffic": live_traffic, "JamsDelay": jams_delay, "JamsLength": jams_length, "JamsCount": jams_count},
        index=time)
    df.index = pd.to_datetime(df.index, unit="ms")
    df.index.name = "Time"
    df.head()

    df_ = pd.read_csv(f"../static/csv/tomtom/{country}.csv", index_col=0, parse_dates=True)

    #print("bebore:"+str(len(df_)))
    #print(df_.index.min())
    df = pd.concat([df,df_])#.drop_duplicates()

    df = df.reset_index().drop_duplicates(subset='Time', keep='last').set_index('Time')

    #print("after:" + str(len(df)))
    #print(df.index.min())
    df = df.sort_values(by=['Time'])
    df.to_csv(f"../static/csv/tomtom/{country}.csv")


for c in cities_be:
    update(c)

for c in cities:
    update(c)







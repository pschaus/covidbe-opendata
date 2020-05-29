import pandas as pd
from datetime import datetime, timedelta
import requests  # Simple HTTP operations (GET and POST)
import os

# upload the device names of the stations into the memory
stations_file = "../static/csv/bike_stations_devices.csv"
stations_pd = pd.read_csv(stations_file)

device_codes = list(stations_pd["device_name"])

# clean the data dir
base_save_dir = "../static/csv/bike_mobility"

current_files = os.listdir(base_save_dir)
if len(current_files):
	for f in current_files:
	    os.remove(f"{base_save_dir}/{f}")

# scrape all data
start_date_h = "startDate=20200201" # enter here the start date of historical scraping
target_date = datetime.utcnow() - timedelta(days=1)
target_date_str = datetime.strftime(target_date, "%Y%m%d")
end_date_h = f"endDate={target_date_str}" # enter here the end date of historical scraping
out_format = "outputFormat=csv" # output format, csv preferred
history_tag = "request=history" # history data

for station in device_codes:
    
    file = "history_data_{}-{}.csv".format(start_date_h, station)
    featureID= "featureID=" + station

    save_file = os.path.join(base_save_dir, file)

    base_url = "https://data-mobility.brussels/bike/api/counts/?&"
    file_url = base_url + "&".join([featureID, start_date_h, end_date_h, out_format, history_tag])
    
    with open(save_file, "wb") as f:
        r = requests.get(file_url)
        total_length = r.headers.get('content-length')
        f.write(r.content)

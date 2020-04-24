import csv
import requests
import urllib
import pandas as pd




from datetime import date
from datetime import timedelta
today = date.today()

# dd/mm/YY
d = (today - timedelta(days=2)).strftime("%Y-%m-%d")
print("day =", d)



DOWNLOAD_URL = f"https://covid19-static.cdn-apple.com/covid19-mobility-data/2006HotfixDev13/v1/en-us/applemobilitytrends-{d}.csv"
DOWNLOAD_PATH ="../static/csv/applemobilitytrends.csv"
urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)






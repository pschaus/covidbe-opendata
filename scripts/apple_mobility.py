import csv
import requests
import urllib
import pandas as pd




from datetime import date
from datetime import timedelta



import urllib.request, json
with urllib.request.urlopen("https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json") as url:
    data = json.loads(url.read().decode())

    DOWNLOAD_URL = "https://covid19-static.cdn-apple.com"+data['basePath']+data['regions']['en-us']['csvPath']

    DOWNLOAD_PATH ="../static/csv/applemobilitytrends.csv"
    urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)
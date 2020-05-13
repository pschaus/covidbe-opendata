import urllib.request
import json
import pandas as pd






DOWNLOAD_URL = "https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv"
DOWNLOAD_PATH ="../static/csv/COVID19BE_CASES_MUNI.csv"
urllib.request.urlretrieve(DOWNLOAD_URL,DOWNLOAD_PATH)

#






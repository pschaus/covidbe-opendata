import hashlib
import locale

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import pandas as pd
import os

import netanalysis.traffic.data.fetch_google_traffic


fetch_google_traffic.main()


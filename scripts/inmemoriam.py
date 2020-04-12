import time
from calendar import monthrange
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import date, datetime
import os.path

def get_link(start, end, page):
    if page == 1:
        page = ""
    else:
        page = f"page={page}&"
    return f'https://www.inmemoriam.be/fr/avis-de-deces/?{page}filter=&periodStart={start}&periodEnd={end}&yearOfBirth=&undertakerId=&placeOfResidence=&provinceId=&newsPaper=&obituary=1'


def gather_for_month(year, month):
    data = []

    start = date(year=year, month=month, day=1)
    end = date(year=year, month=month, day=monthrange(year,month)[1])
    page = 1
    while True:
        attempt = 0
        while True:
            print(start, page, attempt)
            try:
                r = requests.get(get_link(start, end, page), allow_redirects=False)
                if r.status_code == 302:
                    break  # last page
                if r.status_code in [302, 200]:
                    break
                print(r.status_code)
            except Exception as e:
                print(e)
            time.sleep(attempt*5)
            attempt += 1

        if r.status_code == 302:
            break

        soup = BeautifulSoup(r.text, features="lxml")

        print("DONE", start, page, len(soup.find_all('a', attrs={"class": "c-deceased"})))
        assert len(soup.find_all('a', attrs={"class": "c-deceased"})) > 0

        for person in soup.find_all('a', attrs={"class": "c-deceased"}):
            age_span = person.find('span', attrs={"class": "c-deceased__age"})
            if age_span is not None:
                age = int(age_span.text.split(" ")[0])
            else:
                age = -1
            location = person.find('div', attrs={"class": "c-deceased__location"}).text.strip()
            departed = person.find('time', attrs={"class": "c-deceased__date"}).text
            departed = datetime.strptime(departed, "%d/%m/%Y").date()
            data.append((departed, age, location))
        page += 1

    return data


gather_for_years = [
    ("../static/csv/inmemoriam_2019.csv", [2019], range(1, 13), False),
    ("../static/csv/inmemoriam_2020.csv", [2020], range(1, (date.today().month+1) if date.today().year == 2020 else 13), True),
]

for filename, years, months, overwrite in gather_for_years:
    if not overwrite and os.path.exists(filename):
        continue
    data = []
    for y in years:
        for m in months:
            data += gather_for_month(y, m)

    pd.DataFrame(data, columns=['Date', 'Age', 'Location']).to_csv(filename)

import hashlib
import locale

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import pandas as pd
import os

locale.setlocale(locale.LC_ALL, 'fr_FR')

YEAR = 2020


def get_link(page):
    return f"https://www.avis-de-deces.net/avis-de-deces/{page}?nomprenomdefunt&periodedudeces=01%2F01%2F{YEAR}+-+31%2F12%2F{YEAR}&communedudeces&communedudecesDpt&loc"


FNAME = f"../../static/csv/avisdedecesfr_{YEAR}.csv"
if os.path.exists(FNAME):
    data = {d["id"]: (d["age"], d["location"].strip(), d["date"], d["publication"]) for d in pd.read_csv(FNAME).to_dict('records')}
    UPDATE_UNTIL = datetime.strptime(max(d[3] for d in data.values()), "%Y-%m-%d").date() - timedelta(days=10)
else:
    data = {}
    UPDATE_UNTIL = date(year=YEAR, month=1, day=1)

print("UPDATE UNTIL", UPDATE_UNTIL)


def save():
    pd.DataFrame([(a, b, c, d, e) for a, (b, c, d, e) in data.items()],
                 columns=['id', 'age', 'location', 'date', 'publication']).set_index(["id"]).to_csv(FNAME)

last_date = date.today()
page = 0
while last_date >= UPDATE_UNTIL:  # first pass must be done with date(year=2019, month=1, day=1)
    print(f"PAGE {page} {last_date}")
    try:
        r = requests.get(get_link(page), allow_redirects=False)
        if r.status_code == 302:
            break # last page
        if r.status_code != 200:
            raise Exception(r.status_code)
        soup = BeautifulSoup(r.text, features="lxml")

        for person in soup.find_all("a", attrs={"class": "link-avis-annonce"}):
            try:
                link = person.get("href")
                id = hashlib.sha224(link.encode()).hexdigest()
                published = datetime.strptime(person.find("time").text.strip(), "%d/%m/%Y").date()
                location = person.find("span", attrs={"class": "from"}).find("strong").text.strip().split("(")[0].strip()
                death = datetime.strptime(person.find("span", attrs={"class": "deces"}).find_all("strong")[0].text.strip(), "%d %B %Y").date()

                try:
                    age = person.find("span", attrs={"class": "deces"}).find_all("strong")[1].text.strip().split(" ")
                    if age[1] in ["ans", "an"]:
                        age = int(age[0])
                    elif age[1] in ["mois", "jour", "jours"]:
                        age = 0
                    else:
                        raise Exception(age)
                except:
                    age = -1 #unknown

                data[id] = (age, location, death, published)
                last_date = published
            except Exception as e:
                print("----------------")
                print(e)
                print(person)
                print("----------------")
        page += 1

        if page % 100 == 0:
            save()
    except Exception as e:
        # repeat!
        print(e)
        pass

save()

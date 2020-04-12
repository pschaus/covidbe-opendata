import hashlib
import locale

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import pandas as pd

locale.setlocale(locale.LC_ALL, 'fr_FR')

def get_link(page):
    return f"http://necro.sudpresse.be/annonces_par_region/toutes_regions?page={page}"

FNAME = "../static/csv/necrosudpresse.csv"
data = []
last_date = date.today()
page = 0
while last_date >= date(year=2019, month=1, day=1):
    print(f"PAGE {page} {last_date}")
    try:
        r = requests.get(get_link(page), allow_redirects=False)
        if r.status_code != 200:
            raise Exception(r.status_code)
        soup = BeautifulSoup(r.text, features="lxml")

        for person in soup.find("div", attrs={"id": "content-area"}).find("ul").find_all("li"):
            try:
                prenom = person.find("div", attrs={"class": "views-field-field-prenom-value"}).text.strip()

                nom = person.find("div", attrs={"class": "views-field-field-nom-value"}).text.strip()
                age = person.find("div", attrs={"class": "views-field-field-age-value"}).text.strip()[1:-1].split(" ")
                if age[1] in ["ans", "an"]:
                    age = int(age[0])
                elif age[1] in ["mois", "jour", "jours"]:
                    age = 0
                else:
                    raise Exception(age)
                localite = person.find("div", attrs={"class": "views-field-field-localite-value"}).find("span").text[:-1]
                death = person.find("div", attrs={"class": "views-field-field-date-deces-value"}).find("span").text.strip().split(" ")[1:]
                death = datetime.strptime(" ".join(death), "%d %B %Y").date()

                id = hashlib.sha224((prenom+nom+str(death)+str(age)+localite).encode()).hexdigest()

                data.append((id, age, localite, death))
                last_date = death
            except Exception as e:
                print("----------------")
                print(e)
                print(person)
                print("----------------")
        page += 1
        pd.DataFrame(data, columns=['id', 'age', 'location', 'date']).set_index(["id"]).to_csv(FNAME)
    except Exception as e:
        # repeat!
        print(e)
        pass


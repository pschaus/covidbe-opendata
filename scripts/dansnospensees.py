import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import pandas as pd

def get_link(page):
    return f"https://www.dansnospensees.be/handlers/memorialsearch.ashx?lang=fr&period=&name=&bo=00000000-0000-0000-0000-000000000000&m=&postalcode=0&city=&p=100&celeb=false&cp={page}"

FNAME = "../static/csv/dansnopensees.csv"
data = []
last_date = date.today()
page = 1
while last_date >= date(year=2019, month=1, day=1):
    print(f"PAGE {page} {last_date}")
    try:
        r = requests.get(get_link(page), allow_redirects=False)
        if r.status_code != 200:
            raise Exception(r.status_code)
        soup = BeautifulSoup(r.text, features="lxml")
        for person in soup.find_all("article"):
            try:
                id = person.get('id')
                birth_date = datetime.strptime(person.find("li", attrs={"class": "birth"}).text.strip().split(" ")[-1], "%d/%m/%Y").date()
                death_date = datetime.strptime(person.find("li", attrs={"class": "death"}).text.strip().split(" ")[-1], "%d/%m/%Y").date()
                location = " ".join(person.find("li", attrs={"class": "address"}).text.strip().split(" ")[2:])
                data.append((id, birth_date, death_date, location))
                last_date = death_date
            except Exception as e:
                print("----------------")
                print(e)
                print(person)
                print("----------------")
        page += 1
        pd.DataFrame(data, columns=['id', 'birth', 'death', 'location']).set_index(["id"]).to_csv(FNAME)
    except Exception as e:
        # repeat!
        print(e)
        pass



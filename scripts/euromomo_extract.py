import json
import requests
from bs4 import BeautifulSoup


def euromomo():
    # Change this
    OUTPUT_FILE = '../static/json/euromomo.json'

    # Change this if the script breaks
    BASE_PAGE = "https://www.euromomo.eu/graphs-and-maps/"
    JS_FILE_PATTERN = "src-templates-graphs-and-maps-js"

    # First, we need to find the JS link inside the webpage
    r = requests.get(BASE_PAGE)
    if r.status_code != 200:
        raise Exception(f"Cannot reach webpage {BASE_PAGE} {r.status_code}")
    soup = BeautifulSoup(r.text, features="lxml")
    link_to_file = None
    for possible in soup.find_all("link", attrs={"as": "script"}):
        if JS_FILE_PATTERN in possible['href']:
            link_to_file = "https://www.euromomo.eu" + possible['href']
            break

    if link_to_file is None:
        print(f"Could not find a JS file with {JS_FILE_PATTERN} in its name :-(")
        exit(1)

    # Now we have found the file, let's download it and find a large JSON part inside
    try:
        js_file: str = requests.get(link_to_file).text
        pos = 0
        found = []
        while True:
            pos = js_file.find("JSON.parse('", pos)
            if pos == -1:
                break
            end_pos = js_file.find("')", pos)

            content = js_file[pos+len("JSON.parse('"):end_pos]
            assert "'" not in content
            found.append(content)
            pos += 1

        # the biggest JSON part in the file is probably the good one ;-)
        biggest = max(found, key=lambda x: len(x))

        # Load it!
        data = json.loads(biggest)

        # We need a bit of renaming
        def rename_key(key, value):
            if isinstance(value, list):
                if "Belgium" in value:
                    return "countries"
                if "Total" in value:
                    return "age_groups"
            elif isinstance(value, str):
                value = int(value)
                if value <= 52:
                    return "week"
                if value >= 2020:
                    return "year"
            elif isinstance(value, dict):
                if set(value.keys()) == {"counts", "zscores", "weeks"}:
                    return "data_totals"
                if set(value.keys()) == {"data", "years"}:
                    return "excess_mortality"
                if set(value.keys()) == {"data", "weeks"}:
                    if len(value["data"]) == 24:
                        return "z_scores_country_age_groups"
                    if len(value["data"]) >= 276:
                        return "z_scores_country"
            raise Exception("Cannot find valid key name")

        data = {rename_key(k, v): v for k, v in data.items()}

        # Done!
        json.dump(data, open('../static/json/euromomo.json', 'w'))
    except:
        print("EUROMOMO modified something in the JS, you need to adapt the script!")
        raise


#euromomo()
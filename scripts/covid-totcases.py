import urllib.request
import json
import pandas as pd

with open('../static/json/maps/be-centers-covid.json') as json_file:
    centers = json.load(json_file)

cases = {k:0 for k in centers.keys()}

names_fr = {k:v["fr"] for k,v in centers.items()}
names_nl = {k:v["nl"] for k,v in centers.items()}
out = []
with urllib.request.urlopen("https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.json") as url:
        data = json.loads(url.read().decode('latin-1'))
        # some entries have no NIS5
        data = list(filter(lambda x: "NIS5" in x, data))
        for entry in data:
            NIS5 = entry['NIS5']
            ncases = entry['CASES']
            if ncases == "<5":
                ncases = 4
            else:
                ncases = int(ncases)
            out.append((NIS5, ncases, names_fr[NIS5], names_nl[NIS5]))


df_communes = pd.DataFrame(out, columns=["NIS5", "CASES", "FR", "NL"])


# add population info
df_communes_tot = pd.merge(df_communes,
                           pd.read_csv("../static/csv/ins_pop.csv", dtype={"NIS5": str}),
                           left_on='NIS5',
                           right_on='NIS5',
                           how='left')


df_communes_tot.to_csv('../static/csv/be-covid-totcases.csv', index=False)

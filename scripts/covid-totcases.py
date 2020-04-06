import urllib.request, json


with open('../static/json/communes/be-centers.json') as json_file:
    centers = json.load(json_file)

cases = {k:0 for k in centers.keys()}

names_fr = {k:v["fr"] for k,v in centers.items()}
names_nl = {k:v["nl"] for k,v in centers.items()}




with urllib.request.urlopen("https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI_CUM.json") as url:
        data = json.loads(url.read().decode('latin-1'))
        # some entries have no NIS5
        data = list(filter(lambda x: "NIS5" in x, data))
        for entry in data:
            NIS5 = entry['NIS5']
            ncases = entry['CASES']
            if ncases == "<5":
                cases[NIS5] = 4
            else:
                cases[NIS5] = int(ncases)


import csv
with open('../static/csv/be-covid.csv', 'w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["NIS5","CASES","FR","NL"])
    for k,v in cases.items():
        csv_writer.writerow([k,v,names_fr[k],names_nl[k]])



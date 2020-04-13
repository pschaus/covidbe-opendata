import os
import sys
from datetime import date
import pandas as pd

os.chdir(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append('./')
import graphs
import graphs.cases_age_groups
import graphs.cases_per_million
import graphs.cases_per_municipality
import graphs.cases_per_province
import graphs.deaths_age_groups
import graphs.deaths_per_million
import graphs.hopitals
import graphs.obituary
import graphs.overmortality
import graphs.testing

out = []
for name, f in graphs.registered_plots.items():
    print(name)
    key = f"{date.today()}/{name}-800-500.png"
    link = graphs.s3_get_link_and_create_if_needed(key, lambda: f().to_image(format="png", width=800, height=500), "image/png")
    out.append((name, link))

print(out)
pd.DataFrame(out, columns=['name', 'link']).to_csv("static/csv/last_plot_images.csv")

import json
import pandas as pd
import plotly.express as px
from flask_babel import gettext

from graphs import register_plot_for_embedding

data = json.load(open('static/json/euromomo.json'))

def extract_for_country(idx):
    assert data["z_scores_country_age_groups"]["data"][idx]["data"][4]["id"] == "Total"
    return {data["z_scores_country_age_groups"]["weeks"][entry["x"]]: entry["y"] for entry in
            data["z_scores_country_age_groups"]["data"][idx]["data"][4]["data"][0]["data"] if "y" in entry}

zscores_countries = {data["z_scores_country_age_groups"]["data"][idx]["id"]: extract_for_country(idx) for idx in range(len(data["z_scores_country_age_groups"]["data"]))}

df_zscores_countries = pd.DataFrame([
    {"country": c, "year": int(x[0:4]), "week": int(x[5:7]), "zscore": y}
    for c, d in zscores_countries.items()
    for x, y in d.items()
])


@register_plot_for_embedding("euromomo_zscores")
def euromomo_zscores():
    return px.line(df_zscores_countries.loc[df_zscores_countries.year >= 2020],
                   x="week", y="zscore", color='country',
                   labels={"week": gettext("Week"), "country": gettext("Country")}
                   )
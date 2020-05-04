import json
import pandas as pd
import plotly.express as px
from flask_babel import gettext
import plotly.graph_objs as go

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



# --------------------------



be_bl = 2166
be_sd = 68

nl_bl = 3024
nl_sd = 84

fr_bl = 10391
fr_sd = 251

uk_bl = 10954
uk_sd = 154


dates = list(zscores_countries['Belgium'].keys())

be = list(zscores_countries['Belgium'].values())
be = [(be_bl+be_sd*x)/be_bl for x in be]

nl = list(zscores_countries['Netherlands'].values())
nl = [(nl_bl+nl_sd*x)/nl_bl for x in nl]

fr = list(zscores_countries['France'].values())
fr = [(fr_bl+fr_sd*x)/fr_bl for x in fr]

uk = list(zscores_countries['UK (England)'].values())
uk = [(uk_bl+uk_sd*x)/uk_bl for x in uk]

# uk data is starting a bit later than the others
drop = len(be)-len(uk)
be = be[drop:]
nl = nl[drop:]
fr = fr[drop:]
dates = dates[drop:]


df = pd.DataFrame(list(zip(dates,be,nl,fr,uk)),index=range(len(dates)),columns=['Week','Belgium','Netherlands','France','UK'])
df = df[(52*5)-9:]


@register_plot_for_embedding("euromomo_ratio")
def euromomo_ratio():
    be_scatter = go.Scatter(x=df.index, y=df.Belgium, name="Belgium")
    nl_scatter = go.Scatter(x=df.index, y=df.Netherlands, name="Netherlands")
    fr_scatter = go.Scatter(x=df.index, y=df.France, name="France")
    uk_scatter = go.Scatter(x=df.index, y=df.UK, name="UK (England)")


    fig = go.Figure(data=[be_scatter,nl_scatter,fr_scatter,uk_scatter])

    fig.update_layout(xaxis_title=gettext('Week'),
                      yaxis_title=gettext('Overmortality: 2020/baseline'),
                      xaxis=dict(tickmode='array', tickvals=df.index, ticktext=df.Week),
                      title=gettext("Ratio 2020/Baseline"), height=500)


    fig.update_layout(hovermode="x")
    return fig


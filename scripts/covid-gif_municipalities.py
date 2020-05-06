import urllib.request, json
import datetime
import pandas as pd
import numpy as np
import io
import requests
from datetime import datetime, date
import geopandas
import plotly.express as px
import plotly
import pandas as pd
from flask_babel import gettext
import os, shutil

os.mkdir("tmp/")


df_communes_tot = pd.merge(pd.read_csv("../static/csv/be-covid-totcases.csv", dtype={"NIS5": str}),
                           pd.read_csv("../static/csv/ins_pop.csv", dtype={"NIS5": str}),
                           left_on='NIS5',
                           right_on='NIS5',
                           how='left')
    
# We take the third highest number of cases per 1000 as the max value to represent on the map
upper_df_communes_tot = np.sort(1000.0*df_communes_tot.CASES/df_communes_tot.POP)[-3]
df_communes_tot["CASES_PER_1000_POP"] = pd.DataFrame.clip( 1000.0*df_communes_tot.CASES/df_communes_tot.POP , upper=upper_df_communes_tot)
df_communes_timeseries = pd.read_csv('../static/csv/be-covid-timeseries.csv')
geojson_communes = geopandas.read_file('../static/json/communes/be-geojson.json')

df_communes_tot['colorbase'] = df_communes_tot.apply(lambda row: np.log2(row.CASES) if row.CASES != 0 else 0, axis=1)
df_communes_tot['name'] = df_communes_tot.apply(
    lambda row: (row.FR if row.FR == row.NL else f"{row.FR}/{row.NL}").replace("_", " "), axis=1)

for i in range(df_communes_timeseries.shape[1]-1):
    df_communes_timeseries.iloc[:,i+1]=df_communes_timeseries.iloc[:,i+1].rolling(window=7).mean()

print("Generation of the png files...")
for DATE in df_communes_timeseries["DATE"][60:]:
    for NIS5 in df_communes_tot["NIS5"]:
        df_communes_tot.loc[df_communes_tot['NIS5'] == NIS5,'CASES_PER_1000_POP']=pd.DataFrame.clip( 1000.*df_communes_timeseries.loc[df_communes_timeseries['DATE']==DATE, NIS5].iloc[0]/df_communes_tot.loc[df_communes_tot['NIS5'] == NIS5,'POP'] , upper=1 )

    fig = px.choropleth_mapbox(df_communes_tot, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES_PER_1000_POP', color_continuous_scale="magma_r",
                               range_color=(0., 0.5),
                               featureidkey="properties.AdMuKey",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_1000_POP",
                               hover_data=["name", "CASES_PER_1000_POP", "NIS5"],
                               height=500,
                               mapbox_style="carto-positron", zoom=6)
                               #colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']])
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title=""#gettext("Number of cases per 1000 inhabitants")
    fig.layout.coloraxis.colorbar.titleside="right"
    fig.layout.coloraxis.colorbar.ticks="outside"
    fig.layout.coloraxis.colorbar.tickmode="array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[0]}</b><br>%{customdata[1]:.2f} cases per 1000 inhabitants"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=25, b=0), title_text=DATE)
    
    plotly.io.orca.config.port = 8123


print("Generation of the gif")
os.system ("convert -verbose -coalesce -set delay \"%[fx:(t!=n-1)?30:240]\" -loop 0 -density 50 -dispose Background ../static/tmp/2020* ../assets/media/map_cases1000.gif")
shutil.rmtree("tmp/")


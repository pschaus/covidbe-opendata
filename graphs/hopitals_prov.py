import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pages import model_warning, get_translation
import numpy as np

# ---------plot of cases per province------------------------
from flask_babel import gettext

from graphs import register_plot_for_embedding

df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/provinces/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()

df = pd.read_csv('static/csv/be-covid-provinces-all.csv')

dates = df.groupby([df.PROVINCE,df.PROV]).agg({'DATE': ['max']}).reset_index()
dates.columns = dates.columns.get_level_values(0)
dfl = dates.merge(df, how='left', left_on=['DATE','PROV','PROVINCE'],right_on=['DATE','PROV','PROVINCE'])
dfl['HOSPI_PER_100000'] = (dfl.TOTAL_IN/dfl.POP)*100000
dfl = dfl.round({'HOSPI_PER_100000': 2})

def map_hospi(column,title):
    fig = px.choropleth_mapbox(dfl, geojson=geojson_provinces,
                               locations="PROV",
                               color=column,
                               color_continuous_scale="magma_r",
                               featureidkey="properties.proviso",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name=column,
                               hover_data=[column, "POP", "PROVINCE"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr=title,
                                                          en=title)
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(
            gettext(title+":<b>%{customdata[0]}<br>pop:<b>%{customdata[1]}<br><b>%{customdata[2]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig

def scatter_hospi(column,title):
    dfls = dfl.sort_values(by=column, axis=0)
    fig = px.scatter(y=dfls.PROVINCE, x=dfls[column],title=title)
    return fig


def map_hospi_provinces():
    return map_hospi('TOTAL_IN','Total Hospitalizations')

def scatter_hospi_provinces():
    return scatter_hospi('TOTAL_IN','Total Hospitalizations')

def map_hospi_per100K_provinces():
    return map_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')

def scatter_hospi_per100K_provinces():
    return scatter_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')


def total_hospi_provinces():
    return px.line(df, x="DATE", y="TOTAL_IN", color="PROVINCE")

def total_icu_provinces():
    return px.line(df, x="DATE", y="TOTAL_IN_ICU", color="PROVINCE")

def total_hospi_new_in_provinces():
    return px.line(df, x="DATE", y="NEW_IN", color="PROVINCE")

def total_hospi_new_out_provinces():
    return px.line(df, x="DATE", y="NEW_OUT", color="PROVINCE")


from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation

from graphs import register_plot_for_embedding


df = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

df['NIS3'] = df.apply(lambda x: x['NIS5'][:2], axis=1)


df3 = df.groupby([df.NIS3]).agg({'CASES': ['sum'],'POP': ['sum']}).reset_index()
df3.columns = df3.columns.get_level_values(0)
df3['NIS3'] = df3['NIS3'].astype(int)


geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
df_names = pd.DataFrame(geojson.drop(columns='geometry'))
df3 = pd.merge(df3,df_names,left_on='NIS3',right_on='NIS3',how='left')
df3['CASES/HABITANT'] = df3['CASES']/df3['POP']*1000




def map_totcases_admin_region_():
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='CASES', color_continuous_scale="magma_r",
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas",en="Number of cases")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[0]}<br><b>%{customdata[1]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig

map_totcases_admin_region_fig = map_totcases_admin_region_()

@register_plot_for_embedding("map_cases_per_admin_region")
def map_totcases_admin_region():
    return map_totcases_admin_region_fig

def map_cases_per_habittant_admin_region_():
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='CASES/HABITANT', color_continuous_scale="magma_r",
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas / 1000 habitants",en="Number of cases / 1000 inhabitants")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[0]}<br><b>%{customdata[1]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig

map_cases_per_habittant_admin_region_fig = map_cases_per_habittant_admin_region_()

@register_plot_for_embedding("cases_per_habitant_admin_region_inhabitant")
def map_cases_per_habittant_admin_region():
    return map_cases_per_habittant_admin_region_fig
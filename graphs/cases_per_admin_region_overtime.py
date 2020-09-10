from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation

from graphs import register_plot_for_embedding


geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
df3 = pd.read_csv("static/csv/cases_weekly_ins3.csv",encoding='latin1')
df3 = df3[df3.WEEK >= 32]

df3d = pd.read_csv("static/csv/cases_daily_ins3.csv",encoding='latin1')




@register_plot_for_embedding("cases_per_admin_region_inhabitant overtime")
def map_totcases_admin_region_overtime():
    maxv = df3.CASES.max()
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='CASES', color_continuous_scale="magma_r",
                               range_color=(0, maxv),
                               animation_frame="WEEK", animation_group="NIS3",
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES",'CASES_PER_1000HABITANT', "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas",en="Number of cases")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[2]}%</b><br>%{customdata[1]}<br>%{customdata[2]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig




@register_plot_for_embedding("cases_per_habitant_admin_region_inhabitant overtime")
def map_cases_per_habittant_admin_region_overtime():
    maxv = df3.CASES_PER_1000HABITANT.max()
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='CASES_PER_1000HABITANT', color_continuous_scale="magma_r",
                               range_color=(0, maxv),
                               animation_frame="WEEK", animation_group="NIS3",
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES",'CASES_PER_1000HABITANT', "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas / 1000 habitants",en="Number of cases / 1000 inhabitants")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[2]}%</b><br>%{customdata[1]}<br>%{customdata[2]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("cases_per_habitant_admin_region_inhabitant_lastweek")
def map_cases_per_habittant_lastweek():
    geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('9 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('3 days')).date()
    df3d = pd.read_csv("static/csv/cases_daily_ins3.csv", encoding='latin1')
    df3d = df3d[df3d.DATE >= str(cutoff1)]
    df3d = df3d[df3d.DATE <= str(cutoff2)]
    df3d = df3d.groupby([df3d.NIS3, df3d.POP]).agg({'CASES': ['sum']}).reset_index()
    df3d.columns = df3d.columns.get_level_values(0)
    df3d['NIS3'] = df3d['NIS3'].astype(int)
    df3d['CASES_PER_100KHABITANT'] = df3d['CASES'] / df3d['POP'] * 100000
    df3d = pd.merge(df3d, df_names, left_on='NIS3', right_on='NIS3', how='left')

    fig = px.choropleth_mapbox(df3d, geojson=geojson,
                               locations="NIS3",
                               color='CASES_PER_100KHABITANT',
                               range_color=(0, 100),
                               # color_continuous_scale="magma_r",
                               color_continuous_scale=[(0, "green"), (0.14, "green"), (0.15, "yellow"),
                                                       (0.30, "yellow"), (0.31, "orange"), (0.50, "orange"),
                                                       (0.51, "red"), (1, "red")],
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_100KHABITANT",
                               hover_data=["CASES_PER_100KHABITANT", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas/100K past [d-9,d-3] days",
                                                          en="Number of cases/100K past [d-9,d-3] days")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[0]}<br><b>%{customdata[1]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("cases_per_admin_region_inhabitant overtime plot")
def plot_cases_admin_region_overtime():
    return px.line(data_frame=df3, x='WEEK', y='CASES', line_group ='name',color='name')



@register_plot_for_embedding("cases_per_habitant_admin_region_inhabitant overtime plot")
def plot_cases_per_habittant_admin_region_overtime():
    return px.line(data_frame=df3, x='WEEK', y='CASES_PER_1000HABITANT', line_group ='name',color='name')



@register_plot_for_embedding("casesdaily_per_admin_region_inhabitant overtime plot")
def plot_cases_daily_admin_region_overtime():
    return px.line(data_frame=df3d, x='DATE', y='CASES', line_group ='name',color='name')


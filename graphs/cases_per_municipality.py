from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation
import json

from graphs import register_plot_for_embedding

df_communes_tot = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

# We take the third highest number of cases per 1000 as the max value to represent on the map
upper_df_communes_tot = np.sort(1000.0*df_communes_tot.CASES/df_communes_tot.POP)[-3]
df_communes_tot["CASES_PER_100_POP"] = pd.DataFrame.clip( 100.0*df_communes_tot.CASES/df_communes_tot.POP , upper=upper_df_communes_tot)
df_communes_tot = df_communes_tot.round({'CASES_PER_100_POP': 1})

geojson_communes = geopandas.read_file('static/json/communes/be-geojson.json')

df_communes_tot['colorbase'] = df_communes_tot.apply(lambda row: np.log2(row.CASES) if row.CASES != 0 else 0, axis=1)
df_communes_tot['name'] = df_communes_tot.apply(
    lambda row: (row.FR if row.FR == row.NL else f"{row.FR}/{row.NL}").replace("_", " "), axis=1)

df_muni = pd.read_csv("static/csv/COVID19BE_CASES_MUNI.csv",encoding='utf8')
df_muni = df_muni.replace({'CASES': '<5'}, {'CASES': '1'}, regex=True)
df_muni['CASES'] = df_muni['CASES'].astype(int)

df5 = pd.read_csv("static/csv/cases_weekly_ins5.csv",encoding='utf8')
df5 = df5[df5.WEEK >= 32]

today_w = datetime.today().isocalendar()[1]


@register_plot_for_embedding("cases_per_municipality_cases_per_week")
def map_communes_cases_per_week():
    maxv = df5.CASES.max()
    fig = px.choropleth_mapbox(df5, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES', color_continuous_scale="magma_r",
                               range_color=(0, maxv),
                               animation_frame="WEEK", animation_group="NIS5",
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES_PER_100HABITANT", "CASES", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = gettext("Number of cases per week")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext("<b>%{customdata[0]} /1000<br><b>%{customdata[1]} cases <br><b>%{customdata[2]}")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("map_cases_incidence_nis5")
def map_cases_incidence_nis5():
    geojson = geopandas.read_file('static/json/communes/be-geojson.json',encoding='utf8')
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

    df5d = pd.read_csv("static/csv/cases_daily_ins5.csv", encoding='utf8')
    df5d = df5d[df5d.DATE >= str(cutoff1)]
    df5d = df5d[df5d.DATE <= str(cutoff2)]
    df5d = df5d.groupby([df5d.NIS5, df5d.POP, df5d.TX_DESCR_FR]).agg({'CASES': ['sum']}).reset_index()
    df5d.columns = df5d.columns.get_level_values(0)
    df5d['NIS5'] = df5d['NIS5'].astype(str)
    df5d['INCIDENCE'] = df5d['CASES'] / df5d['POP'] * 100000
    df5d = df5d.round({'INCIDENCE': 1})

    fig = px.choropleth_mapbox(df5d, geojson=geojson,
                               locations="NIS5",
                               color='INCIDENCE',
                               range_color=(0, 500),
                               color_continuous_scale="magma_r",
                               #color_continuous_scale=[(0, "green"), (15/150, "green"), (15/150, "yellow"),
                               #                        (30/150, "yellow"), (30/150, "orange"), (50/150, "orange"),
                               #                        (50/150, "red"), (100/150, "red"),(100/150, "black"),(150/150, "black")],
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="TX_DESCR_FR",
                               hover_data=["INCIDENCE", "POP", "TX_DESCR_FR"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas/100K past [d-17,d-4] days",
                                                          en="Number of cases/100K past [d-17,d-4] days")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("bubble_map_cases_incidence_nis5")
def bubble_map_cases_incidence_nis5():
    geojson = geopandas.read_file('static/json/communes/be-geojson.json', encoding='utf8')
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

    df5d = pd.read_csv("static/csv/cases_daily_ins5.csv", encoding='utf8')
    df5d = df5d[df5d.DATE >= str(cutoff1)]
    df5d = df5d[df5d.DATE <= str(cutoff2)]
    df5d = df5d.groupby([df5d.NIS5, df5d.POP, df5d.TX_DESCR_FR]).agg({'CASES': ['sum']}).reset_index()
    df5d.columns = df5d.columns.get_level_values(0)
    df5d['NIS5'] = df5d['NIS5'].astype(str)
    df5d['INCIDENCE'] = df5d['CASES'] / df5d['POP'] * 100000
    df5d = df5d.round({'INCIDENCE': 1})

    f = open('static/json/communes/be-centroids.geojson', "r")
    data = json.loads(f.read())
    res = [(x['properties']['NIS5'], x['geometry']['coordinates'][0], x['geometry']['coordinates'][1]) for x in
           data['features']]
    df = pd.DataFrame(res, columns=['NIS5', 'lon', 'lat'])
    df5d = pd.merge(df5d, df, left_on='NIS5', right_on='NIS5', how='left')

    fig = px.scatter_mapbox(df5d, lat="lat", lon="lon", color="INCIDENCE", size="POP",
                            color_continuous_scale="magma_r", zoom=6, range_color=(0, 1500),
                            hover_data=["INCIDENCE", "POP"],
                            hover_name="TX_DESCR_FR",
                            mapbox_style="carto-positron", height=600, )
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas/100K past [d-17,d-4] days",
                                                          en="Number of cases/100K past [d-17,d-4] days")
    fig.update_coloraxes(colorbar_title_side='right')
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig

@register_plot_for_embedding("cases_per_municipality_per_100inhabitant_per_week")
def map_communes_per_100inhabitant_per_week():
    maxv = df5.CASES_PER_100HABITANT.max()
    fig = px.choropleth_mapbox(df5, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES_PER_100HABITANT', color_continuous_scale="magma_r",
                               range_color=(0, maxv),
                               animation_frame="WEEK", animation_group="NIS5",
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES_PER_100HABITANT", "CASES", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = gettext("Number of cases per 1000 habitants per week")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext("<b>%{customdata[0]} /100<br><b>%{customdata[1]} cases <br><b>%{customdata[2]}")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig



@register_plot_for_embedding("map_communes_per_inhabitant")
def map_communes_per_inhabitant():
    fig = px.choropleth_mapbox(df_communes_tot, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES_PER_100_POP', color_continuous_scale="magma_r",
                               #range_color=(3, 10),
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="name",
                               hover_data=["name", "CASES_PER_100_POP","NIS5"],
                               height=500,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title=get_translation(fr="Pourcentage de cas dans la population depuis mars",
                                                          en="Pourcentage de cas dans la population depuis mars")
    fig.layout.coloraxis.colorbar.titleside="right"
    fig.layout.coloraxis.colorbar.ticks="outside"
    fig.layout.coloraxis.colorbar.tickmode="array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))

    return fig


@register_plot_for_embedding("map_communes")
def map_communes():
    fig = px.choropleth_mapbox(df_communes_tot, geojson=geojson_communes,
                               locations="NIS5",
                               color='colorbase', color_continuous_scale="deep",
                               range_color=(3, 10),
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["name", "CASES", "NIS5"],
                               height=500,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    NB_TICKS = 12
    fig.layout.coloraxis.colorbar = dict(
        title=gettext("Number of cases"),
        titleside="right",
        tickmode="array",
        tickvals=list(range(1, NB_TICKS + 1)),
        ticktext=[str(2 ** i) for i in range(1, NB_TICKS + 1)],
        ticks="outside"
    )
    fig.update_traces(
        hovertemplate=gettext("<b>%{customdata[0]}</b><br>%{customdata[1]} cases")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("barplot_communes")
def barplot_communes(commune_nis=73006):
    df_com = df_muni[df_muni.NIS5 == commune_nis]
    descr = df_com['TX_DESCR_FR'].values
    title = "municipality"
    if len(descr) > 0:
        title = descr[0]
    cases = sum(df_com.CASES.values)
    fig = px.bar(x=df_com.DATE, y=df_com.CASES)

    fig.update_layout(title_text=gettext("Number of cases in {title}: {cases}").format(title=title, cases=cases),
                      height=500, template="plotly_white", margin=dict(l=20, r=0, t=60, b=0))
    fig.layout.coloraxis.showscale = False
    fig.update_yaxes(title="cases (1 = <5)")

    fig.update_traces(
        hovertemplate=gettext("<b>%{x}</b><extra>%{y} cases</extra>"),
    )
    return fig



@register_plot_for_embedding("map_bubble_communes_since_beginning")
def map_bubble_communes_since_beginning():
    geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))

    f = open('static/json/communes/be-centroids.geojson', "r")
    data = json.loads(f.read())
    res = [(x['properties']['NIS5'], x['geometry']['coordinates'][0], x['geometry']['coordinates'][1]) for x in
           data['features']]
    df = pd.DataFrame(res, columns=['NIS5', 'lon', 'lat'])

    df_communes_tot = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

    df = pd.merge(df_communes_tot, df, left_on='NIS5', right_on='NIS5', how='left')

    df['CASES_PERCENTAGE'] = 100 * df['CASES'] / df['POP']
    df = df.round({'CASES_PERCENTAGE': 1})


    fig = px.scatter_mapbox(df, lat="lat", lon="lon", color="CASES_PERCENTAGE", size="POP",
                            color_continuous_scale="magma_r", zoom=6, range_color=(0, 10),
                            hover_data=["CASES_PERCENTAGE", "POP"],
                            hover_name="FR",
                            mapbox_style="carto-positron", height=600, )
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Pourcentage de cas dans la population depuis mars",
                                                          en="Pourcentage de cas dans la population depuis mars")
    fig.update_coloraxes(colorbar_title_side='right')

    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))

    return fig



@register_plot_for_embedding("bubble_map_cases_incidence_nis5")
def bubble_map_cases_incidence_nis5():
    geojson = geopandas.read_file('static/json/communes/be-geojson.json', encoding='utf8')
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

    df5d = pd.read_csv("static/csv/cases_daily_ins5.csv", encoding='utf8')
    df5d = df5d[df5d.DATE >= str(cutoff1)]
    df5d = df5d[df5d.DATE <= str(cutoff2)]
    df5d = df5d.groupby([df5d.NIS5, df5d.POP, df5d.TX_DESCR_FR]).agg({'CASES': ['sum']}).reset_index()
    df5d.columns = df5d.columns.get_level_values(0)
    df5d['NIS5'] = df5d['NIS5'].astype(str)
    df5d['INCIDENCE'] = df5d['CASES'] / df5d['POP'] * 100000
    df5d = df5d.round({'INCIDENCE': 1})

    f = open('static/json/communes/be-centroids.geojson', "r")
    data = json.loads(f.read())
    res = [(x['properties']['NIS5'], x['geometry']['coordinates'][0], x['geometry']['coordinates'][1]) for x in
           data['features']]
    df = pd.DataFrame(res, columns=['NIS5', 'lon', 'lat'])
    df5d = pd.merge(df5d, df, left_on='NIS5', right_on='NIS5', how='left')

    fig = px.scatter_mapbox(df5d, lat="lat", lon="lon", color="INCIDENCE", size="POP",
                            color_continuous_scale="magma_r", zoom=6, range_color=(0, 500),
                            hover_data=["INCIDENCE", "POP"],
                            hover_name="TX_DESCR_FR",
                            mapbox_style="carto-positron", height=600, )
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas/100K past [d-17,d-4] days",
                                                          en="Number of cases/100K past [d-17,d-4] days")
    fig.update_coloraxes(colorbar_title_side='right')
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


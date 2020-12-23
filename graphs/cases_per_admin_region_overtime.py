from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation
import plotly.graph_objects as go
from graphs import register_plot_for_embedding


geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
df3 = pd.read_csv("static/csv/cases_weekly_ins3.csv",encoding='utf8')
#df3 = df3[df3.WEEK >= 32]

df3d = pd.read_csv("static/csv/cases_daily_ins3.csv",encoding='utf8')




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


def dfoff(offset):
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta(str(17 + offset) + ' days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta(str(4 + offset) + ' days')).date()

    df3d = pd.read_csv("static/csv/cases_daily_ins3.csv", encoding='latin1')
    df3d = df3d[df3d.DATE >= str(cutoff1)]
    df3d = df3d[df3d.DATE <= str(cutoff2)]
    df3d = df3d.groupby([df3d.NIS3, df3d.POP]).agg({'CASES': ['sum']}).reset_index()
    df3d.columns = df3d.columns.get_level_values(0)
    df3d['NIS3'] = df3d['NIS3'].astype(int)
    df3d['CASES_PER_100KHABITANT'] = df3d['CASES'] / df3d['POP'] * 100000
    df3d = pd.merge(df3d, df_names, left_on='NIS3', right_on='NIS3', how='left')
    df3d = df3d.round({'CASES_PER_100KHABITANT': 1})

    df3d = df3d.sort_values(by='CASES_PER_100KHABITANT', axis=0)
    return df3d


@register_plot_for_embedding("scattter-incidence-nis3")
def scatter_incidence_nis3():
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))

    # title = get_translation(fr="Nombres de cas/100K past [d-17,d-4] days",en="Number of cases/100K past [d-17,d-4] days")

    df1 = dfoff(0)
    df2 = dfoff(5)
    df = df1.merge(df2, left_on=['NIS3', 'POP', 'name'], right_on=['NIS3', 'POP', 'name'])
    df['increase5d'] = ((df['CASES_PER_100KHABITANT_x'] / df['CASES_PER_100KHABITANT_y']) - 1) * 100

    df = df.sort_values(by='CASES_PER_100KHABITANT_x', axis=0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(y=df.name, x=df['CASES_PER_100KHABITANT_x'],
                             name="[t-17,t-4]", mode='markers',
                             marker=dict(
        color=df['increase5d'], #set color equal to a variable
        size = 12,
        cmin=-50,
        cmax=50,
        colorscale=[
                [0, "#238b45"],
                [0.25, "#238b45"],
                [0.25, "#66c2a4"],
                [0.50, "#66c2a4"],
                [0.50, "#fb6a4a"],
                [0.75, "#fb6a4a"],
                [0.75, "#cb181d"],
                [1, "#cb181d"]],
        showscale=True
    )))

    fig.add_trace(go.Scatter(y=df.name, x=df['CASES_PER_100KHABITANT_y'],
                             name="[t-22,t-9]", mode='markers', marker_color='black'))

    fig.update_layout(autosize=True, height=900)
    fig.update_layout(template="plotly_white")

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title="Incidence evolution over 5 days (color = % increase/decrease)",
    )

    return fig


@register_plot_for_embedding("map_cases_incidence_nis3")
def map_cases_incidence_nis3():
    geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
    df_names = pd.DataFrame(geojson.drop(columns='geometry'))
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

    df3d = pd.read_csv("static/csv/cases_daily_ins3.csv", encoding='latin1')
    df3d = df3d[df3d.DATE >= str(cutoff1)]
    df3d = df3d[df3d.DATE <= str(cutoff2)]
    df3d = df3d.groupby([df3d.NIS3, df3d.POP]).agg({'CASES': ['sum']}).reset_index()
    df3d.columns = df3d.columns.get_level_values(0)
    df3d['NIS3'] = df3d['NIS3'].astype(int)
    df3d['CASES_PER_100KHABITANT'] = df3d['CASES'] / df3d['POP'] * 100000
    df3d = pd.merge(df3d, df_names, left_on='NIS3', right_on='NIS3', how='left')
    df3d = df3d.round({'CASES_PER_100KHABITANT': 1})

    fig = px.choropleth_mapbox(df3d, geojson=geojson,
                               locations="NIS3",
                               color='CASES_PER_100KHABITANT',
                               range_color=(0, 500),
                               color_continuous_scale="magma_r",
                               #color_continuous_scale=[(0, "green"), (15/150, "green"), (15/150, "yellow"),
                               #                        (30/150, "yellow"), (30/150, "orange"), (50/150, "orange"),
                               #                        (50/150, "red"), (100/150, "red"),(100/150, "black"),(150/150, "black")],
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_100KHABITANT",
                               hover_data=["CASES_PER_100KHABITANT", "POP", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr="Nombres de cas/100K past [d-17,d-4] days",
                                                          en="Number of cases/100K past [d-17,d-4] days")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(
            gettext("incidence:<b>%{customdata[0]}<br>pop:<b>%{customdata[1]}<br><b>%{customdata[2]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig


@register_plot_for_embedding("cases_per_admin_region_inhabitant overtime plot")
def plot_cases_admin_region_overtime():
    fig = px.line(data_frame=df3, x='WEEK', y='CASES', line_group ='name',color='name')
    fig.update_layout(template="plotly_white")
    return fig



@register_plot_for_embedding("cases_per_habitant_admin_region_inhabitant overtime plot")
def plot_cases_per_habittant_admin_region_overtime():
    df3d['CASES_PER_1000HABITANT'] = df3d['CASES']/df3d['POP']*100000
    fig = px.bar(data_frame=df3d, x='DATE', y='CASES_PER_1000HABITANT',color='name')
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("casesdaily_per_admin_region_inhabitant overtime plot")
def plot_cases_daily_admin_region_overtime():
    fig = px.bar(data_frame=df3d, x='DATE', y='CASES',color='name')
    fig.update_layout(template="plotly_white")
    return fig



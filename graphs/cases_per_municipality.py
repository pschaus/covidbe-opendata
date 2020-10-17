from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation

from graphs import register_plot_for_embedding

df_communes_tot = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

# We take the third highest number of cases per 1000 as the max value to represent on the map
upper_df_communes_tot = np.sort(1000.0*df_communes_tot.CASES/df_communes_tot.POP)[-3]
df_communes_tot["CASES_PER_1000_POP"] = pd.DataFrame.clip( 1000.0*df_communes_tot.CASES/df_communes_tot.POP , upper=upper_df_communes_tot)

df_communes_timeseries = pd.read_csv('static/csv/be-covid-timeseries.csv')
geojson_communes = geopandas.read_file('static/json/communes/be-geojson.json')

df_communes_tot['colorbase'] = df_communes_tot.apply(lambda row: np.log2(row.CASES) if row.CASES != 0 else 0, axis=1)
df_communes_tot['name'] = df_communes_tot.apply(
    lambda row: (row.FR if row.FR == row.NL else f"{row.FR}/{row.NL}").replace("_", " "), axis=1)


df5 = pd.read_csv("static/csv/cases_weekly_ins5.csv",encoding='latin1')
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
                               hover_data=["CASES_PER_1000HABITANT", "CASES", "name"],
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
    geojson = geopandas.read_file('static/json/communes/be-geojson.json')
    cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
    cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

    df5d = pd.read_csv("static/csv/cases_daily_ins5.csv", encoding='latin1')
    df5d = df5d[df5d.DATE >= str(cutoff1)]
    df5d = df5d[df5d.DATE <= str(cutoff2)]
    df5d = df5d.groupby([df5d.NIS5, df5d.POP, df5d.TX_DESCR_FR]).agg({'CASES': ['sum']}).reset_index()
    df5d.columns = df5d.columns.get_level_values(0)
    df5d['NIS5'] = df5d['NIS5'].astype(str)
    df5d['CASES_PER_100KHABITANT'] = df5d['CASES'] / df5d['POP'] * 100000
    df5d = df5d.round({'CASES_PER_100KHABITANT': 1})

    fig = px.choropleth_mapbox(df5d, geojson=geojson,
                               locations="NIS5",
                               color='CASES_PER_100KHABITANT',
                               range_color=(0, 1500),
                               color_continuous_scale="magma_r",
                               #color_continuous_scale=[(0, "green"), (15/150, "green"), (15/150, "yellow"),
                               #                        (30/150, "yellow"), (30/150, "orange"), (50/150, "orange"),
                               #                        (50/150, "red"), (100/150, "red"),(100/150, "black"),(150/150, "black")],
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_100KHABITANT",
                               hover_data=["CASES_PER_100KHABITANT", "POP", "TX_DESCR_FR"],
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



@register_plot_for_embedding("cases_per_municipality_per_1000inhabitant_per_week")
def map_communes_per_1000inhabitant_per_week():
    maxv = df5.CASES_PER_1000HABITANT.max()
    fig = px.choropleth_mapbox(df5, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES_PER_1000HABITANT', color_continuous_scale="magma_r",
                               range_color=(0, maxv),
                               animation_frame="WEEK", animation_group="NIS5",
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES",
                               hover_data=["CASES_PER_1000HABITANT", "CASES", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = gettext("Number of cases per 1000 habitants per week")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext("<b>%{customdata[0]} /1000<br><b>%{customdata[1]} cases <br><b>%{customdata[2]}")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig



@register_plot_for_embedding("cases_per_municipality_per_inhabitant")
def map_communes_per_inhabitant():
    fig = px.choropleth_mapbox(df_communes_tot, geojson=geojson_communes,
                               locations="NIS5",
                               color='CASES_PER_1000_POP', color_continuous_scale="magma_r",
                               #range_color=(3, 10),
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_1000_POP",
                               hover_data=["name", "CASES_PER_1000_POP", "NIS5"],
                               height=500,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title=gettext("Number of cases per 1000 inhabitants")
    fig.layout.coloraxis.colorbar.titleside="right"
    fig.layout.coloraxis.colorbar.ticks="outside"
    fig.layout.coloraxis.colorbar.tickmode="array"
    fig.update_traces(
        hovertemplate=gettext(gettext("<b>%{customdata[0]}</b><br>%{customdata[1]:.2f} cases per 1000 inhabitants"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))

    return fig


@register_plot_for_embedding("cases_per_municipality")
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


def barplot_communes(commune_nis=73006):
    [nis, cases, fr, nl, _, title_text, _, _] = df_communes_tot.loc[df_communes_tot['NIS5'] == str(commune_nis)].values[0]
    title = title_text

    orig_first_date = datetime.strptime(
        df_communes_timeseries.loc[df_communes_timeseries[str(commune_nis)] > 0]["DATE"].min(), "%Y-%m-%d").date()
    first_date = date(year=orig_first_date.year, month=orig_first_date.month, day=1)
    last_date = datetime.strptime(df_communes_timeseries["DATE"].max(), "%Y-%m-%d").date()

    range_y_stop = max(10, df_communes_timeseries[str(commune_nis)].max())

    fig = px.bar(df_communes_timeseries, x='DATE', y=str(commune_nis), height=400,
                 range_x=(first_date, last_date),
                 range_y=(0, range_y_stop),
                 color=str(commune_nis), color_continuous_scale="deep",
                 labels={"DATE": "Date", str(commune_nis): "# Cases"})

    fig.update_layout(title_text=gettext("Number of cases in {title}: {cases}").format(title=title, cases=cases),
                      height=500, template="plotly_white", margin=dict(l=20, r=0, t=60, b=0))
    fig.layout.coloraxis.showscale = False
    fig.update_traces(
        hovertemplate=gettext("<b>%{x}</b><extra>%{y} cases</extra>"),
    )
    return fig

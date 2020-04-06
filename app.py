import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


import urllib.request, json

import plotly.express as px

import pandas as pd

from graphs.cases_per_municipality import map_communes, barplot_communes

df_communes_tot = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})
df_communes_timeseries = pd.read_csv('static/csv/be-covid-timeseries.csv')
df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')
df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')
df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv')

# ---------plot of cases per province------------------------

with open('static/json/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()
map_provinces = px.choropleth_mapbox(df_prov_tot, geojson=geojson_provinces,
                                     locations="PROVINCE",
                                     color='CASES_PER_THOUSAND', color_continuous_scale="Viridis",
                                     range_color=(range_min, range_max),
                                     featureidkey="properties.proviso",
                                     center={"lat": 50.85045, "lon": 4.34878},
                                     hover_name="CASES_PER_THOUSAND",
                                     height=900,
                                     mapbox_style="carto-positron", zoom=7)


# ---------plot of cases per province------------------------

with open('static/json/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.HOSPI_PER_CASES.min()
range_max = df_prov_tot.HOSPI_PER_CASES.max()
map_provinces_hospi_per_cases = px.choropleth_mapbox(df_prov_tot, geojson=geojson_provinces,
                                     locations="PROVINCE",
                                     color='HOSPI_PER_CASES', color_continuous_scale="Viridis",
                                     range_color=(range_min,range_max),
                                     featureidkey="properties.proviso",
                                     center={"lat": 50.85045, "lon": 4.34878},
                                     hover_name="HOSPI_PER_CASES",
                                     height=900,
                                     mapbox_style="carto-positron", zoom=7)





# ---------bar plot age groups cases---------------------------

idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
# bar plot with bars per age groups
bars_provinces = []
provinces = sorted(df_prov_timeseries.PROVINCE_NAME.unique())
for p in provinces:
    df_p = df_prov_timeseries.loc[df_prov_timeseries['PROVINCE_NAME'] == p]
    df_p = df_p.groupby(['DATE']).agg({'CASES': 'sum'})
    df_p.index = pd.DatetimeIndex(df_p.index)
    df_p = df_p.reindex(idx, fill_value=0)
    bars_provinces.append(go.Bar(
        x=df_p.index,
        y=df_p['CASES'],
        name=p
    ))
fig_provinces_cases = go.Figure(data=bars_provinces,
                                 layout=go.Layout(barmode='group'), )
fig_provinces_cases.update_layout(height=1000, )


# ---------bar plot age groups cases---------------------------

idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
# bar plot with bars per age groups
bars_age_groups = []
age_groups = sorted(df_prov_timeseries.AGEGROUP.unique())
for ag in age_groups:
    df_ag = df_prov_timeseries.loc[df_prov_timeseries['AGEGROUP'] == ag]
    df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
    df_ag.index = pd.DatetimeIndex(df_ag.index)
    df_ag = df_ag.reindex(idx, fill_value=0)
    bars_age_groups.append(go.Bar(
        x=df_ag.index,
        y=df_ag['CASES'],
        name=ag
    ))
fig_age_groups_cases = go.Figure(data=bars_age_groups,
                                 layout=go.Layout(barmode='group'), )
fig_age_groups_cases.update_layout(height=1000, )




# ---------bar plot age groups death---------------------------

idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
# bar plot with bars per age groups
bars_age_groups_deaths = []
age_groups = sorted(df_mortality.AGEGROUP.unique())
for ag in age_groups:
    df_ag = df_mortality.loc[df_mortality['AGEGROUP'] == ag]
    df_ag = df_ag.groupby(['DATE']).agg({'DEATHS': 'sum'})
    df_ag.index = pd.DatetimeIndex(df_ag.index)
    df_ag = df_ag.reindex(idx, fill_value=0)
    bars_age_groups_deaths.append(go.Bar(
        x=df_ag.index,
        y=df_ag['DEATHS'],
        name=ag
    ))
fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths,
                                       layout=go.Layout(barmode='group'),)
fig_age_groups_deaths.update_layout(height=1000,)


# ---------------------------------------------


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(children=[
    html.H1(children='COVID-DATA',),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='map-prov', figure=map_provinces), ),

        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='map_provinces_hospi_per_cases', figure=map_provinces_hospi_per_cases), ),

        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='barplot-prov', figure=fig_provinces_cases), ),

        ]
    ),
    dbc.Row(
        [
            dcc.Graph(id='bar_age_groups_cases',
                      figure=fig_age_groups_cases
                      )
        ]),
    dbc.Row(
        [
            dcc.Graph(id='bar_age_groups_deaths',
                      figure=fig_age_groups_deaths
                      )
        ]),
])


# ---------------callbacks-----------------------





if __name__ == '__main__':
    app.run_server(debug=True)

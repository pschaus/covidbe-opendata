import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
from graphs import register_plot_for_embedding

import numpy as np
import altair as alt
from pages import get_translation


from datetime import datetime

import pandas
import geopandas

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')

df = pandas.read_csv("static/csv/mortality_statbel.csv",parse_dates=['DT_DATE'], date_parser=dateparse)



df.dropna(thresh=1,inplace=True)

def week(date):
    return date.isocalendar()[1]



df = df[df['DT_DATE'] >= '2019-12-30']


df['week'] = df.apply(lambda x: week(x['DT_DATE']), axis=1)
df_week = df.groupby(['NR_YEAR','week','CD_AGEGROUP'])["MS_NUM_DEATH"].sum().reset_index()
df_week.rename(columns={"MS_NUM_DEATH": "tot","NR_YEAR": "year","CD_AGEGROUP": "age"},inplace=True)

def death_age_groups(barmode="group"):
    """
    bar plot age group death in belgium
    """

    age_groups = ['0-24', '25-44', '45-64', '65-74', '75-84', '85+']
    bars_age_groups_deaths = []

    for ag in age_groups:
        df_ag = df_week.loc[df_week['age'] == ag]
        bars_age_groups_deaths.append(go.Bar(
            x=df_ag.week,
            y=df_ag['tot'],
            name=ag
        ))

    maxw = df_week.loc[df_week['week'].idxmax()]['week']
    fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths,
                                      layout=go.Layout(barmode=barmode), )

    # Set x-axis title
    fig_age_groups_deaths.update_xaxes(title_text="Week")

    # Set y-axes titles
    fig_age_groups_deaths.update_yaxes(title_text=get_translation(en="Total Deaths",fr="Nombre de morts"))

    fig_age_groups_deaths.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                                        title=get_translation(en="Weekly Total deaths per age group in Belgium 2020",fr="Nombre de morts dans chaque groupe d'age en Belgique 2020 "))
    return fig_age_groups_deaths

geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
df3 = pd.read_csv("static/csv/weekly_mortality_statbel_ins3.csv")


@register_plot_for_embedding("death_arrondissements_map_weekly")
def death_arrondissements_map_weekly():
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='DEATH_PER_1000HABITANT', color_continuous_scale="magma_r",
                               range_color=(0.06, 0.3),
                               animation_frame="WEEK", animation_group="NIS3",
                               featureidkey="properties.NIS3",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name='DEATH_PER_1000HABITANT',
                               hover_data=["DEATH_PER_1000HABITANT", "TOT", "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(en="Number of deaths / 1000 inhabitants",fr="Nombre de morts / 1000 habitants")
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext("<b>%{customdata[0]} /1000</b><br><b>%{customdata[1]}</b><br><b>%{customdata[2]}</b>")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig
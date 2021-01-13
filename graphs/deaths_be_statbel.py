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


geojson = geopandas.read_file('static/json/admin-units/be-geojson.geojson')
df3 = pd.read_csv("static/csv/yearly_mortality_statbel_ins3.csv")



@register_plot_for_embedding("death_arrondissements_map_yearly")
def death_arrondissements_map_yearly():
    fig = px.choropleth_mapbox(df3, geojson=geojson,
                               locations="NIS3",
                               color='DEATH_PER_1000HABITANT', color_continuous_scale="magma_r",
                               range_color=(9, 14),
                               animation_frame="YEAR", animation_group="NIS3",
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
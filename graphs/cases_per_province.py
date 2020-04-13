import json
import pandas as pd
import plotly.express as px

# ---------plot of cases per province------------------------
from flask_babel import gettext

from graphs import register_plot_for_embedding

df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/provinces/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()


@register_plot_for_embedding("cases_per_province_map")
def map_provinces():
    fig = px.choropleth_mapbox(df_prov_tot,
                               geojson=geojson_provinces,
                               locations="PROVINCE",
                               color='CASES_PER_THOUSAND',
                               color_continuous_scale="deep",
                               range_color=(range_min, range_max),
                               featureidkey="properties.proviso",
                               center={"lat": 50.641111, "lon": 4.668889},
                               height=400,
                               mapbox_style="carto-positron",
                               zoom=6,
                               labels={'CASES_PER_THOUSAND': gettext('Cases per thousand inhabitants')}
                               )

    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.titleside = 'right'
    fig.update_traces(
        hovertemplate=gettext("<b>%{properties.name}</b><br>%{z:.3f} cases per 1000 inhabitants")
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=0, b=0))
    return fig


@register_plot_for_embedding("cases_per_province_bar")
def barplot_provinces_cases():
    fig = px.bar(df_prov_tot,
                 y='PROVINCE_NAME',
                 x='CASES_PER_THOUSAND',
                 color='CASES_PER_THOUSAND',
                 orientation='h',
                 color_continuous_scale="deep",
                 range_color=(range_min, range_max),
                 hover_name="PROVINCE_NAME",
                 labels={'CASES_PER_THOUSAND': gettext('Cases per thousand inhabitants')},
                 height=400)
    fig.update_traces(
        hovertemplate=gettext("<b>%{y}</b><br>%{x:.3f} cases per 1000 inhabitants"),
        textposition='outside',
        texttemplate='%{x:.3f}'
    )
    fig.layout.coloraxis.colorbar.titleside = 'right'
    fig.layout.yaxis.title = ""
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig

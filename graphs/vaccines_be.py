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


df=pd.read_csv('static/csv/be-covid-vaccines.csv') # last line is NaN
print(df)
df_A = df.loc[df['DOSE'].isin(['A','C'])]
df_B = df[df.DOSE == 'B']

df_A = df_A.groupby(['DATE']).agg({'COUNT': 'sum'})
df_B = df_B.groupby(['DATE']).agg({'COUNT': 'sum'})

#df = pd.read_csv('static/csv/be-covid-vaccines.csv')  # last line is NaN

df_AC = df.loc[df['DOSE'].isin(['A', 'C'])]

df_ag = df_AC.groupby(['DATE', 'REGION', 'AGEGROUP']).agg({'COUNT': 'sum'}).reset_index()
df_ag = df_ag.replace({'Ostbelgien':'Wallonia'})
#print(df_ag.REGION.unique())



df_ag_regions = pd.read_csv('static/csv/age-group-regions.csv')  # last line is NaN
df_ag = pd.merge(df_ag, df_ag_regions, left_on=['REGION', 'AGEGROUP'], right_on=['REGION', 'AGEGROUP'])
df_ag["percent"] = 100 * df_ag['COUNT'] / df_ag['POP']




def trace(region, ag, legend=False, color="red"):
    df_ = df_ag[df_ag.REGION == region]
    df_ = df_[df_.AGEGROUP == ag]

    return go.Scatter(x=df_.DATE, y=df_.percent.cumsum(), name=region, legendgroup=region, showlegend=legend,
                      marker_color=color)


def add_ag(fig,ag, row, col, legend=False):
    colors = px.colors.qualitative.Plotly
    i = 0
    for r in ['Wallonia', "Flanders", "Brussels"]:
        fig.add_trace(trace(r, ag, color=colors[i], legend=legend), row, col)
        i += 1

@register_plot_for_embedding("vaccines_ag_region")
def fig_ag_dose_a_c():
    fig = make_subplots(rows=4, cols=2, subplot_titles=('85+', '75-84', '65-74', '55-64', '45-54', '35-44','18-34'))

    fig.update_layout(template="plotly_white")

    add_ag(fig,"85+", 1, 1, legend=True)
    add_ag(fig,"75-84", 1, 2)
    add_ag(fig,"65-74", 2, 1)
    add_ag(fig,"55-64", 2, 2)
    add_ag(fig,"45-54", 3, 1)
    add_ag(fig,"35-44", 3, 2)
    add_ag(fig,"18-34", 4, 1)

    for i in range(1, 8):
        fig['layout']['yaxis' + str(i)].update(title='', range=[0, 100], autorange=False)

    fig.update_layout(template="plotly_white", height=700)

    fig.update_layout(yaxis_range=[0, 100])
    return fig


@register_plot_for_embedding("vaccines_daily")
def plot_vaccines_cumulated():
    """
    plot of the cumulated vaccines
    """
    fig = make_subplots(specs=[[{"secondary_y": True, }]], shared_yaxes='all', shared_xaxes='all')

    fig.add_trace(
        go.Scatter(x=df_A.index, y=df_A.COUNT.cumsum(), name=gettext('Cumulated DOSE A or C')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_B.index, y=df_B.COUNT.cumsum(), name=gettext('Cumulated DOSE B')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=df_A.index, y=df_A.COUNT, name=gettext('Daily DOSE A or C')),
        secondary_y=True,
    )

    fig.add_trace(
        go.Bar(x=df_B.index, y=df_B.COUNT, name=gettext('Daily DOSE B')),
        secondary_y=True,
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="Cumulated", secondary_y=False)
    fig.update_yaxes(title_text="Daily", secondary_y=True)

    fig.update_layout(title=gettext("Vaccines Belgium"))
    fig.update_layout(template="plotly_white")
    fig.update_layout(yaxis_range=[0, max(df_A.COUNT.cumsum().values)])
    return fig






df_ag_nis =pd.read_csv("static/csv/vaccines_age_group_nis5.csv",sep=",",encoding='latin') # last line is NaN

from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation
import json

from graphs import register_plot_for_embedding


def vaccine_nis5(age_group):
    geojson = geopandas.read_file('static/json/communes/be-geojson.json', encoding='utf8')

    fig = px.choropleth_mapbox(df_ag_nis[df_ag_nis.AgeGroup == age_group], geojson=geojson,
                               locations="NIS5",
                               color='percent',
                               range_color=(0, 100),
                               color_continuous_scale="magma_r",
                               featureidkey="properties.NIS5",
                               center={"lat": 50.641111, "lon": 4.668889},
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = "Percentage of vaccination " + age_group
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    #fig.update_layout(title="Percentage of vaccination " + age_group)

    return fig


@register_plot_for_embedding("vaccines_ag_region")
def show_brand():
    df=pd.read_csv('static/csv/be-covid-vaccines.csv') # last line is NaN
    df_A = df.loc[df['DOSE'].isin(['A','C'])]
    df_A = df_A.groupby(['DATE','BRAND']).agg({'COUNT': 'sum'}).reset_index()


    fig = go.Figure()

    for b in df_A.BRAND.unique():
        df_b = df_A[df_A.BRAND == b]


        fig.add_trace(go.Scatter(x=df_b.DATE, y=df_b.COUNT.cumsum(), name=b, legendgroup=b))

    fig.update_layout(template="plotly_white", height=600)
    fig.update_layout(title="First doses (A or C) total per brand")
    return fig
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pages import model_warning, get_translation

# ---------plot of cases per province------------------------
from flask_babel import gettext

from graphs import register_plot_for_embedding

df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/provinces/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()



df = pd.read_csv('static/csv/be-covid-provinces-all.csv')
df['POSITIVE_RATE'] = df['CASES']/df['TESTS_ALL']
df['TESTING_RATE'] = df['TESTS_ALL']/df['POP']


cutoff1 = (pd.to_datetime('today') - pd.Timedelta('17 days')).date()
cutoff2 = (pd.to_datetime('today') - pd.Timedelta('4 days')).date()

df3d = df[df.DATE >= str(cutoff1)]
df3d = df3d[df3d.DATE <= str(cutoff2)]
df3d = df3d.groupby([df3d.PROVINCE, df3d.POP,df3d.PROV]).agg({'CASES': ['sum']}).reset_index()
df3d.columns = df3d.columns.get_level_values(0)
df3d['CASES_PER_100KHABITANT'] = df3d['CASES'] / df3d['POP'] * 100000
df3d = df3d.round({'CASES_PER_100KHABITANT': 1})


def df_prov_avg_age_cases():
    df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')
    age_group_weight = {'0-9': 5, '10-19': 15, '20-29': 25, '30-39': 35, '40-49': 45, '50-59': 55,
                        '60-69': 65, '70-79': 75, '80-89': 85, '90+': 90}

    df_prov_timeseries['weight'] = df_prov_timeseries['AGEGROUP'].map(age_group_weight)
    df_prov_timeseries['weightedcases'] = df_prov_timeseries['weight'] * df_prov_timeseries['CASES']
    df_prov = df_prov_timeseries.groupby(
        [df_prov_timeseries.DATE, df_prov_timeseries.PROVINCE, df_prov_timeseries.PROVINCE_NAME]).agg(
        {'CASES': ['sum'], 'weightedcases': ['sum']}).reset_index()
    df_prov.columns = df_prov.columns.get_level_values(0)
    df_prov['avg_age'] = df_prov['weightedcases'] / df_prov['CASES']
    df_prov['PROVINCE'] = df_prov['PROVINCE_NAME']
    return df_prov

df_prov = df_prov_avg_age_cases()

def bar_testing_provinces():
    return px.bar(df, x="DATE", y="CASES", color="PROVINCE", barmode="stack")

def bar_cases_provinces():
    return px.bar(df, x="DATE", y="CASES", color="PROVINCE", barmode="stack")


import numpy as np

def plot(df,column_name,title):
    def moving_average(a, n=1) :
        a = a.astype(np.float)
        ret = np.cumsum(a)
        ret[n:] = ret[n:] - ret[:-n]
        ret[:n-1] = ret[:n-1]/range(1,n)
        ret[n-1:] = ret[n - 1:] / n
        return ret


    bars = []
    provinces = sorted(df.PROVINCE.unique())
    for p in provinces:
        df_p = df.loc[df['PROVINCE'] == p]
        bars.append(go.Scatter(
            x=df_p.DATE,
            y=moving_average(df_p[column_name].values,7),
            name=p
        ))


    fig = go.Figure(data=bars,layout=go.Layout(barmode='group'),)
    fig.update_layout(template="plotly_white", height=500,margin=dict(l=0, r=0, t=30, b=0), title=title)
    return fig


def avg_age_cases_provinces():
    return plot(df_prov,'avg_age','average age of cases (avg 7 days)')

def avg_testing_provinces():
    return plot(df,'TESTS_ALL',"Testing avg 7 days")

def avg_cases_provinces():
    return plot(df,'CASES',"Cases avg 7 days")

def avg_positive_rate_provinces():
    return plot(df,'POSITIVE_RATE',"Positive rate avg 7 days")

def avg_testing_per_habbitant_provinces():
    return plot(df,'TESTING_RATE',"TESTING rate = number of tests/inhabitant (avg 7 days)")

def map_cases_incidence_provinces():
    fig = px.choropleth_mapbox(df3d, geojson=geojson_provinces,
                               locations="PROV",
                               color='CASES_PER_100KHABITANT',
                               range_color=(0, 150),
                               #color_continuous_scale="magma_r",
                               color_continuous_scale=[(0, "green"), (15/150, "green"), (15/150, "yellow"),
                                                       (30/150, "yellow"), (30/150, "orange"), (50/150, "orange"),
                                                       (50/150, "red"), (100/150, "red"),(100/150, "black"),(150/150, "black")],
                               featureidkey="properties.proviso",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name="CASES_PER_100KHABITANT",
                               hover_data=["CASES_PER_100KHABITANT", "POP", "PROVINCE"],
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





def scatter_incidence_provinces():
    df3ds = df3d.sort_values(by='CASES_PER_100KHABITANT', axis=0)
    fig = px.scatter(y=df3ds.PROVINCE, x=df3ds.CASES_PER_100KHABITANT,title="Incidence rate [d-17,d-4]")
    def add_line(x,col):
        fig.add_shape(
                    type="line",
                    x0=x,
                    x1 =x,
                    y0 = 0,
                    y1 = 10,
                    line = {
                     "color":col,
                     "width":1,
                    }
                )
    add_line(0,'green')
    add_line(15,'yellow')
    add_line(30,'orange')
    add_line(50,'red')
    add_line(100,'black')
    return fig





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

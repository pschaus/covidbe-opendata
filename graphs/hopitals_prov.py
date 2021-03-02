import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pages import model_warning, get_translation
import numpy as np

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots
from scipy import stats
import numpy as np
from graphs import register_plot_for_embedding


# ---------plot of cases per province------------------------
from flask_babel import gettext

from graphs import register_plot_for_embedding

df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/provinces/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()

df = pd.read_csv('static/csv/be-covid-provinces-all.csv')
df.sort_values(by=['DATE'], inplace=True, ascending=True)
df['TOTAL_IN_PER_100K'] = df['TOTAL_IN'] / df['POP'] * 100000
df['NEW_IN_PER_100K'] = df['NEW_IN'] / df['POP'] * 100000

dates = df.groupby([df.PROVINCE,df.PROV]).agg({'DATE': ['max']}).reset_index()
dates.columns = dates.columns.get_level_values(0)
dfl = dates.merge(df, how='left', left_on=['DATE','PROV','PROVINCE'],right_on=['DATE','PROV','PROVINCE'])
dfl['HOSPI_PER_100000'] = (dfl.TOTAL_IN/dfl.POP)*100000
dfl = dfl.round({'HOSPI_PER_100000': 2})

def map_hospi(column,title):
    fig = px.choropleth_mapbox(dfl, geojson=geojson_provinces,
                               locations="PROV",
                               color=column,
                               color_continuous_scale="magma_r",
                               featureidkey="properties.proviso",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name=column,
                               hover_data=[column, "POP", "PROVINCE"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr=title,
                                                          en=title)
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(
        hovertemplate=gettext(
            gettext(title+":<b>%{customdata[0]}<br>pop:<b>%{customdata[1]}<br><b>%{customdata[2]}"))
    )
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig



def scatter_hospi(column,title):
    dfls = dfl.sort_values(by=column, axis=0)
    fig = px.scatter(y=dfls.PROVINCE, x=dfls[column],title=title,labels={"x":"number of hospitalizations","y":""})
    return fig

@register_plot_for_embedding("map_hospi_provinces")
def map_hospi_provinces():
    return map_hospi('TOTAL_IN','Total Hospitalizations')


@register_plot_for_embedding("scatter_hospi_provinces")
def scatter_hospi_provinces():
    fig = scatter_hospi('TOTAL_IN','Total Hospitalizations')
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("map_hospi_per100K_provinces")
def map_hospi_per100K_provinces():
    return map_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')

@register_plot_for_embedding("scatter_hospi_per100K_provinces")
def scatter_hospi_per100K_provinces():
    fig = scatter_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("total_hospi_provinces")
def total_hospi_provinces():
    fig = px.bar(df, x="DATE", y="TOTAL_IN", color="PROVINCE",title="Total number of hospitalized patients at the moment of reporting")
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("total_icu_provinces")
def total_icu_provinces():
    fig = px.bar(df, x="DATE", y="TOTAL_IN_ICU", color="PROVINCE",title="Total number of hospitalized patients in ICU at the moment of reporting")
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("total_hospi_new_in_provinces")
def total_hospi_new_in_provinces():
    fig = px.bar(df, x="DATE", y="NEW_IN", color="PROVINCE",title="Number of hospital intakes that day")
    fig.update_layout(template="plotly_white")
    return fig

@register_plot_for_embedding("total_hospi_new_out_provinces")
def total_hospi_new_out_provinces():
    fig = px.bar(df, x="DATE", y="NEW_OUT", color="PROVINCE",title="Number of hospital discharges that day")
    fig.update_layout(template="plotly_white")
    return fig


def hospi_prov(fig, row, col, fromw2, prov=None, show_legend=False):
    df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')

    if prov is not 'All':
        df_hospi = df_hospi[df_hospi['PROVINCE_NAME'] == prov]

    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum', 'TOTAL_IN_ICU': 'sum'})

    x2 = df.index[df.index >= fromw2]
    y2 = df.NEW_IN[df.index >= fromw2]

    df.index = pd.to_datetime(df.index)
    dw = df.index[df.index >= fromw2].dayofweek
    colors_map = {0: '#fccde5', 1: '#8dd3c7', 2: '#b3de69', 3: '#bebada', 4: '#fb8072', 5: '#fdb462', 6: '#80b1d3',
                  7: 'lightgrey'}
    colors = [colors_map[i] for i in dw]

    wave2 = go.Bar(x=x2, y=y2, name=gettext('NEW_IN'), legendgroup='group2', showlegend=False, marker_color=colors)
    fig.add_trace(wave2, row, col)

    fig.add_trace(go.Scatter(x=x2, y=y2.rolling(7).mean(), showlegend=show_legend, name=gettext('avg past 7 days'),
                             legendgroup='avg 7 days', marker_color="red"), row, col)

    slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(0, 14), y2[-14:])
    # print(prov,slope, intercept, r_value, p_value, std_err )
    # print(p_value)
    ylin_interp = np.arange(0, 14) * slope + intercept
    fig.add_trace(go.Scatter(x=x2[-14:], y=ylin_interp, showlegend=show_legend, name=gettext('Linear Interp'),
                             legendgroup='linear-interp', marker_color="orange"), row, col)

    fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0))

    return fig


@register_plot_for_embedding("hospi_new_in_provinces")
def hospi_new_in_per_provinces():
    fig = make_subplots(rows=4, cols=3, subplot_titles=(
        'Liège', 'Namur', 'Luxembourg', 'Hainaut', 'Brussels', 'BrabantWallon', 'VlaamsBrabant', 'OostVlaanderen',
        'WestVlaanderen', 'Limburg', 'Antwerpen', 'All'))

    fw2 = '2021-02-01'

    hospi_prov(fig, 1, 1, fromw2=fw2, prov='Liège', show_legend=True)
    hospi_prov(fig, 1, 2, fromw2=fw2, prov='Namur')
    hospi_prov(fig, 1, 3, fromw2=fw2, prov='Luxembourg')
    hospi_prov(fig, 2, 1, fromw2=fw2, prov='Hainaut')
    hospi_prov(fig, 2, 2, fromw2=fw2, prov='Brussels')
    hospi_prov(fig, 2, 3, fromw2=fw2, prov='BrabantWallon')
    hospi_prov(fig, 3, 1, fromw2=fw2, prov='VlaamsBrabant')
    hospi_prov(fig, 3, 2, fromw2=fw2, prov='OostVlaanderen')
    hospi_prov(fig, 3, 3, fromw2=fw2, prov='WestVlaanderen')
    hospi_prov(fig, 4, 1, fromw2=fw2, prov='Limburg')
    hospi_prov(fig, 4, 2, fromw2=fw2, prov='Antwerpen')
    hospi_prov(fig, 4, 3, fromw2=fw2, prov='All')

    title = "New daily Hospitalizations per Province"

    fig.update_layout(template="plotly_white", height=800, margin=dict(l=50, r=50, t=50, b=50),
                      title=gettext(title))
    return fig


@register_plot_for_embedding("hospi_provinces_per100k")
def hospi_provinces_per100k():
    fig = px.line(df, x="DATE", y='TOTAL_IN_PER_100K', color="PROVINCE",title="Total number of hospitalized patients per 100K habitants")
    fig.update_layout(template="plotly_white")
    fig.update_layout(
    hovermode='x unified',
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[{"yaxis.type": "linear"}],
                    label="LINEAR",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log"}],
                    label="LOG",
                    method="relayout"
                )
            ]),
        ),
    ])
    return fig



def plot(df,column_name,title):
    bars = []
    provinces = df.PROVINCE.unique()
    for p in provinces:
        df_p = df.loc[df['PROVINCE'] == p]
        bars.append(go.Scatter(
            x=df_p.DATE,
            y=df_p[column_name].rolling(7).mean(),
            name=p
        ))


    fig = go.Figure(data=bars,layout=go.Layout(barmode='group'),)
    fig.update_layout(template="plotly_white", height=500,margin=dict(l=0, r=0, t=30, b=0), title=title)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear"}],
                        label="LINEAR",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log"}],
                        label="LOG",
                        method="relayout"
                    )
                ]),
            ),
        ])
    return fig



@register_plot_for_embedding("new_in_per_100K_provinces")
def new_in_per_100K_provinces():
    return plot(df,'NEW_IN_PER_100K',"NEW_IN / 100K inhabitant (avg 7 days)")
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


def hospi_w1w2(fig, row, col, fromw2, prov=None, show_legend=False):
    df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')

    if prov is not None:
        df_hospi = df_hospi[df_hospi['PROVINCE_NAME'] == prov]

    def df_hospi_death():
        df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')
        idx = pd.date_range(df_hospi.DATE.min(), df_hospi.DATE.max())
        df_hospi = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'TOTAL_IN_ICU': 'sum', 'NEW_IN': 'sum'})
        df_hospi.index = pd.DatetimeIndex(df_hospi.index)
        df_hospi = df_hospi.reindex(idx, fill_value=0)

        df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)
        idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
        df_mortality = df_mortality.groupby(['DATE']).agg({'DEATHS': 'sum'})
        df_mortality.index = pd.DatetimeIndex(df_mortality.index)
        df_mortality = df_mortality.reindex(idx, fill_value=0)

        df = df_mortality.merge(df_hospi, how='left', left_index=True, right_index=True)

        df = df[df.index >= '2020-03-15']
        return df

    import numpy as np

    def moving_average(a, n=1):
        a = a.astype(np.float)
        ret = np.cumsum(a)
        ret[n:] = ret[n:] - ret[:-n]
        ret[:n - 1] = ret[:n - 1] / range(1, n)
        ret[n - 1:] = ret[n - 1:] / n
        return ret

    df = df_hospi_death()

    # print(df_hospi)

    """
    bar plot hospitalization
    """
    df = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum', 'NEW_OUT': 'sum', 'NEW_IN': 'sum', 'TOTAL_IN_ICU': 'sum'})

    n = 30

    x1 = df.index.values[:n]
    x2 = df.index.values[df.index >= fromw2]
    y1 = df.TOTAL_IN[:n]
    y2 = df.TOTAL_IN[df.index >= fromw2]

    values = y2.values
    doubling = 1
    while values[-doubling] > values[-1] / 2 and doubling < len(values) - 1:
        doubling += 1

    wave1 = go.Bar(y=y1, name=gettext('Wave1'), legendgroup='group1', showlegend=show_legend, marker_color="red")
    wave2 = go.Bar(y=y2, name=gettext('Wave2'), legendgroup='group2', showlegend=show_legend, marker_color="blue")

    fig.add_trace(wave1, row, col)
    fig.add_trace(wave2, row, col)

    fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0))

    xvals = list(range(0, len(x2), 5))
    # xlabels = [x1[v][-5:]+"|"+x2[v][-5:] for v in xvals]
    xlabels = [x2[v][-5:] for v in xvals]

    ymax = max(y2.values)
    xdoubling = len(y2) - doubling
    line = go.layout.Shape(type="line", x0=xdoubling, y0=0, x1=xdoubling, y1=ymax,
                           line=dict(color="lightblue", width=3))
    fig.add_shape(line, row=row, col=col)

    fig.update_xaxes(tickmode='array', tickvals=xvals, ticktext=xlabels, row=row, col=col)

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=xvals,
            ticktext=xlabels,
        ),

    )
    return fig

@register_plot_for_embedding("hospi_w1w2_provinces")
def hospi_w1w2_provinces():
    fig = make_subplots(rows=4, cols=3, subplot_titles=(
    'Liège', 'Namur', 'Luxembourg', 'Hainaut', 'Brussels', 'BrabantWallon', 'VlaamsBrabant', 'OostVlaanderen',
    'WestVlaanderen', 'Limburg', 'Antwerpen'))

    hospi_w1w2(fig,1,1,fromw2 = '2020-10-01', prov = 'Liège',show_legend=True)
    hospi_w1w2(fig, 1, 2, fromw2='2020-10-01', prov='Namur')
    hospi_w1w2(fig, 1, 3, fromw2='2020-10-01', prov='Luxembourg')
    hospi_w1w2(fig, 2, 1, fromw2='2020-10-01', prov='Hainaut')
    hospi_w1w2(fig, 2, 2, fromw2='2020-10-01', prov='Brussels')
    hospi_w1w2(fig, 2, 3, fromw2='2020-10-01', prov='BrabantWallon')
    hospi_w1w2(fig, 3, 1, fromw2='2020-10-01', prov='VlaamsBrabant')
    hospi_w1w2(fig, 3, 2, fromw2='2020-10-01', prov='OostVlaanderen')
    hospi_w1w2(fig, 3, 3, fromw2='2020-10-01', prov='WestVlaanderen')
    hospi_w1w2(fig, 4, 1, fromw2='2020-10-01', prov='Limburg')
    hospi_w1w2(fig, 4, 2, fromw2='2020-10-01', prov='Antwerpen')

    title = "Hospitalization First Wave vs Second Wave "

    fig.update_layout(template="plotly_white", height=800, margin=dict(l=50, r=50, t=50, b=50),
                      title=gettext(title))
    return fig




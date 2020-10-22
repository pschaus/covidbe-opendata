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


def map_hospi_provinces():
    return map_hospi('TOTAL_IN','Total Hospitalizations')

def scatter_hospi_provinces():
    fig = scatter_hospi('TOTAL_IN','Total Hospitalizations')
    fig.update_layout(template="plotly_white")
    return fig

def map_hospi_per100K_provinces():
    return map_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')

def scatter_hospi_per100K_provinces():
    fig = scatter_hospi('HOSPI_PER_100000','Total Hospitalizations per 100K inhabitants')
    fig.update_layout(template="plotly_white")
    return fig


def total_hospi_provinces():
    fig = px.bar(df, x="DATE", y="TOTAL_IN", color="PROVINCE",title="Total number of hospitalized patients at the moment of reporting")
    fig.update_layout(template="plotly_white")
    return fig

def total_icu_provinces():
    fig = px.bar(df, x="DATE", y="TOTAL_IN_ICU", color="PROVINCE",title="Total number of hospitalized patients in ICU at the moment of reporting")
    fig.update_layout(template="plotly_white")
    return fig

def total_hospi_new_in_provinces():
    fig = px.bar(df, x="DATE", y="NEW_IN", color="PROVINCE",title="Number of hospital intakes that day")
    fig.update_layout(template="plotly_white")
    return fig

def total_hospi_new_out_provinces():
    fig = px.bar(df, x="DATE", y="NEW_OUT", color="PROVINCE",title="Number of hospital discharges that day")
    fig.update_layout(template="plotly_white")
    return fig


def hospi_w1w2(fig, row, col, fromw2, prov=None):
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

    wave1 = go.Bar(y=df.TOTAL_IN[:n], name=gettext('#Total Hospitalized Wave1'), legendgroup='group1', showlegend=False,
                   marker_color="red")
    wave2 = go.Bar(y=df.TOTAL_IN[df.index >= fromw2], name=gettext('#Total Hospitalized Wave2'), legendgroup='group1',
                   showlegend=False, marker_color="blue")

    # wave1 = go.Bar(y=df.TOTAL_IN_ICU[:n], name=gettext('#Total Hospitalized Wave1'),legendgroup='group1',showlegend=False,marker_color="red")
    # wave2 = go.Bar(y=df.TOTAL_IN_ICU[df.index>=fromw2], name=gettext('#Total Hospitalized Wave2'),legendgroup='group1',showlegend=False,marker_color="blue")

    fig.add_trace(wave1, row, col)
    fig.add_trace(wave2, row, col)
    # fig_hospi = go.Figure(data=[wave1,wave2], layout=go.Layout(barmode='group'), )

    # fig_hospi = go.Figure(data=[wave1,wave2,wave1_ICU,wave2_ICU], layout=go.Layout(barmode='group'), )

    fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0))

    # fig.update_layout(xaxis_title=gettext('Day'),
    #                        yaxis_title=gettext('Number of / Day'))

    xvals = list(range(0, n, 5))
    xlabels = [df.index[:n][v] for v in xvals]

    fig.update_xaxes(tickmode='array', tickvals=xvals, ticktext=xlabels, row=row, col=col)

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=xvals,
            ticktext=xlabels,
        ),

    )
    return fig


def hospi_w1w2_provinces():
    fig = make_subplots(rows=4, cols=3, subplot_titles=(
    'Liège', 'Namur', 'Luxembourg', 'Hainaut', 'Brussels', 'BrabantWallon', 'VlaamsBrabant', 'OostVlaanderen',
    'WestVlaanderen', 'Limburg', 'Antwerpen'))

    hospi_w1w2(fig, 1, 1, fromw2='2020-10-01', prov='Liège')
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




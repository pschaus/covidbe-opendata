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
df.sort_values(by=['DATE'], inplace=True, ascending=True)
df['TOTAL_IN_PER_100K'] = df['TOTAL_IN'] / df['POP'] * 100000

pop = {'Brussels': 1218255, 'Flanders': 6629143, 'Wallonia': 3645243}



@register_plot_for_embedding("hospi_region_per100k")
def hospi_region_per100k(column,avg=False):
    barmode = 'stack'  # group
    # bar plot with bars per age groups
    bars = []
    regions = sorted(df.REGION.unique())

    idx = pd.date_range(df.DATE.min(), df.DATE.max())

    for r in regions:
        df_r = df.loc[df['REGION'] == r]
        df_r = df_r.groupby(['DATE']).agg({column: 'sum'})
        df_r.index = pd.DatetimeIndex(df_r.index)
        df_r = df_r.reindex(idx, fill_value=0)

        if avg:
            plot = go.Scatter(x=df_r.index, y=(100000 * df_r[column] / pop[r]).rolling(7).mean(), name=r)
        else:
            plot = go.Scatter(x=df_r.index, y=(100000 * df_r[column] / pop[r]), name=r)
        bars.append(plot)

    fig = go.Figure(data=bars,
                    layout=go.Layout(barmode='group'), )
    fig.update_layout(template="plotly_white", height=500, barmode=barmode, margin=dict(l=0, r=0, t=30, b=0), )

    fig.update_layout(template="plotly_white", title=column+" per 100K inhabitants" + ("(avg 7 days)" if avg  else ""))
    fig.update_layout(
        hovermode='x unified',
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

@register_plot_for_embedding("hospi_total_in_region_per100k")
def hospi_total_in_region_per100k():
    return hospi_region_per100k("TOTAL_IN",avg=False)


@register_plot_for_embedding("hospi_total_in_icu_region_per100k")
def hospi_total_in_icu_region_per100k():
    return hospi_region_per100k("TOTAL_IN_ICU",avg=False)


@register_plot_for_embedding("hospi_newin_region_per100k")
def hospi_newin_region_per100k():
    return hospi_region_per100k("NEW_IN",avg=True)


@register_plot_for_embedding("hospi_newout_region_per100k")
def hospi_newout_region_per100k():
    return hospi_region_per100k("NEW_OUT",avg=True)
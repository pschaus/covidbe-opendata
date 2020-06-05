
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

import pandas as pd
import plotly.graph_objs as go
from flask_babel import gettext

from datetime import datetime
import plotly.express as px
import os

mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M")

df = pd.read_csv(f'static/csv/tunnels_bxl.csv', parse_dates=['from', 'to'], date_parser=mydateparser)

mask = (df['from'] >= '2020-02-1')
df = df.loc[mask]

mask = (df['from'] <= '2020-05-19')
df = df.loc[mask]

df.reset_index(level=0, inplace=True)
df.set_index('from', inplace=True)


def fig_tunnel(weekday=True, time='07:00'):
    df_ = df.between_time(time, time)
    if weekday:
        df_ = df_[df_.index.dayofweek < 5]
    else:
        df_ = df_[df_.index.dayofweek == 5]
    df_.reset_index(level=0, inplace=True)

    fig = px.line(df_, x="from", y="volume", color="tunnel")

    fig.update_layout(
        xaxis_title="day",
        yaxis_title="#vehicles"
    )
    return fig


def fig_tunnel_ratio(weekday=True, time='07:00'):
    df_ = df.between_time(time, time)
    if weekday:
        df_ = df_[df_.index.dayofweek < 5]
    else:
        df_ = df_[df_.index.dayofweek == 5]
    df_.reset_index(level=0, inplace=True)

    mask = (df_['from'] <= '2020-03-10')
    df2 = df_.loc[mask]

    df2 = df2.groupby('tunnel').mean()

    dict_mean = df2.to_dict()['volume']

    df_['rel_volume'] = df_.apply(lambda row: row['volume'] / dict_mean[row['tunnel']], axis=1)

    fig = px.line(df_, x="from", y="rel_volume", color="tunnel")

    fig.update_layout(
        xaxis_title="day",
        yaxis_title="ratio wrt to normality"
    )
    return fig


def fig_global_tunnel_ratio(weekday=True, time='07:00'):
    df_ = df.between_time(time, time)
    if weekday:
        df_ = df_[df_.index.dayofweek < 5]
    else:
        df_ = df_[df_.index.dayofweek == 5]
    df_.reset_index(level=0, inplace=True)

    df_day = df_.groupby([df_['from'].dt.date]).agg({'volume': ['sum']}).reset_index()
    df_day.columns = df_day.columns.get_level_values(0)

    df_day.reset_index(level=0, inplace=True)
    df_day['from'] = pd.to_datetime(df_day['from'])
    mask = (df_day['from'] <= '2020-03-10')

    df2 = df_day.loc[mask]
    mean = df2['volume'].mean()

    df_day['rel_volume'] = df_day.volume / mean
    fig = px.line(df_day, x="from", y="rel_volume")

    fig.update_layout(
        xaxis_title="day",
        yaxis_title="ratio wrt to normality"
    )
    return fig


@register_plot_for_embedding("brussels-tunnels")
def brussels_tunnels():
    fig1 = fig_tunnel(True, '07:00')
    fig1.update_layout(title="#Tunnel Traffic of Brussels at 7:00-8:00 Workdays")
    return fig1


@register_plot_for_embedding("brussels-tunnels-ratio")
def brussels_tunnels_ratio():
    fig1 = fig_tunnel_ratio(True, '07:00')
    fig1.update_layout(title="#Tunnel Traffic of Brussels at 7:00-8:00 Workdays")
    return fig1


@register_plot_for_embedding("brussels-tunnels-ratio")
def brussels_alltunnels_ratio():
    fig1 = fig_global_tunnel_ratio(True, '07:00')
    fig1.update_layout(title="#Total Tunnel Traffic of Brussels at 7:00-8:00 Workdays")
    return fig1



# -------------------------------------------------------------

cities =  ['Brussels','Paris','Amsterdam','Berlin','London']

df_apple = pd.read_csv(f'static/csv/applemobilitytrends.csv')

cdf = df_apple[df_apple["geo_type"] == "city"]


def df_country(country):
    cdf_c = cdf.loc[cdf['region'] == country]
    cdf_c = cdf_c.drop(labels=['geo_type','region','alternative_name','sub-region','country'], axis = 1)
    cdf_c.rename(columns={'transportation_type': 'date'},inplace=True)
    cdf_c.set_index(['date'])
    cdf_c=cdf_c.T
    cdf_c.index.name = 'date'
    cdf_c.columns = cdf_c.iloc[0]
    cdf_c.drop(cdf_c.index[0],inplace=True)
    return cdf_c



cities_df = {c:df_country(c) for c in cities}

@register_plot_for_embedding("apple_mobility_plot_cities")
def apple_mobility_plot_cities():
    colors = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'  # blue-teal
    ]

    graphs = ['driving', 'transit', 'walking', ]
    large_fig = make_subplots(rows=len(graphs), cols=1, subplot_titles=graphs, horizontal_spacing=0.05,
                              vertical_spacing=0.02, shared_xaxes=True)
    r = 1
    for g in graphs:

        fig = go.Figure()
        a = 0
        for c in cities:
            df = cities_df[c]
            large_fig.append_trace(
                go.Scatter(x=df.index, y=df[g], line=dict(color=colors[a]), mode='lines', name=c, legendgroup=c,
                           showlegend=(r == 1)), row=r, col=1)
            a += 1

        r += 1

    large_fig['layout'].update(height=1000, title='Apple Mobility Reports')
    return large_fig

# -------------------------------------------------------------

bike_data_dir = f'static/csv/bike_mobility'
all_bike_files = sorted([f for f in os.listdir(bike_data_dir) if "history" in f])

stations_pd = pd.read_csv(f"static/csv/bike_stations_devices.csv")
station_names = [s.split(" - ")[-1] for s in stations_pd["road_nl"]]
device_codes = list(stations_pd["device_name"])
devices = {dc: sn for dc, sn in zip(device_codes, station_names)}

@register_plot_for_embedding("bike_mobility_plot_stations")
def bike_mobility_plot_stations():
    # global bike_data_dir

    fig = go.Figure()
    for bike_file_name in all_bike_files:
        station_code = bike_file_name.split("-")[-1].split(".")[0]
        station_name = devices[station_code]

        bike_file = f"{bike_data_dir}/{bike_file_name}"
        bike_pd = pd.read_csv(bike_file)
        count_by_date = bike_pd.groupby(["Date"]).sum()
        count_by_date.drop(columns = ["Time gap", "Average speed"], inplace = True)
        count_by_date.index = pd.to_datetime(count_by_date.index, yearfirst = True, format = "%Y-%m-%d")

        mask = (count_by_date.index <= '2020-03-10')

        count_before_deconfinement = count_by_date.loc[mask]
        mean = count_before_deconfinement['Count'].mean()
        count_by_date['rel_count'] = count_by_date.Count / mean
        fig.add_scatter(x=count_by_date.index, y=count_by_date["rel_count"], mode='lines', 
                                    name=station_name, # legendgroup=c, # line=dict(color=colors[a]),
                                   showlegend=True)
    fig['layout'].update(height=500, title='Bike Mobility Brussels Reports')
    return fig



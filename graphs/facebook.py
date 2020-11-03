from graphs import register_plot_for_embedding
from pages import get_translation

import pandas as pd
import geopandas
import plotly.express as px
from flask_babel import get_locale, gettext
import plotly.graph_objs as go
import json

df_population = pd.read_csv('static/csv/facebook/population.csv')
df_movement_range = pd.read_csv('static/csv/facebook/movement-range.csv')


def shorten(x):
    if x == 'Arr. de Bruxelles-Capitale/Arr. van Brussel-Hoofdstad':
        return 'Bruxelles-Capitale'
    if x == 'Arr. Verviers - communes francophones':
        return 'Verviers (FR)'
    if x == 'Bezirk Verviers - Deutschsprachige Gemeinschaft':
        return 'Verviers (GE)'
    return x[5:]


df_movement_range_short = df_movement_range.copy()
df_movement_range_short.name = df_movement_range_short.name.apply(shorten)

df_baseline = df_population.loc[(df_population.date_time >= '2020-04-20') & (df_population.date_time < '2020-04-27')]
df_baseline = df_baseline.drop(['n_crisis', 'percent_change'], axis=1)


def remove_arrondissement(name):
    if name[:18] == 'Arrondissement de ':
        return name[18:]
    elif name[:17] == 'Arrondissement d\'':
        return name[17:]
    elif name[:15] == 'Arrondissement ':
        return name[15:]


df_translation = pd.read_csv("static/csv/ins.csv")
df_translation = df_translation.loc[(df_translation.INS >= 10000) &
                                    (df_translation.INS % 1000 == 0) &
                                    (df_translation.INS % 10000 != 0)]
df_translation.FR = df_translation.FR.apply(remove_arrondissement)
df_translation.NL = df_translation.NL.apply(remove_arrondissement)
df_translation.drop(['Langue'], axis=1, inplace=True)


def translate(name):
    if name in df_translation.NL.unique():
        return df_translation.loc[df_translation.NL == name].iloc[0].FR
    else:
        return name


df_baseline.name = df_baseline.name.apply(translate)

# changes of 2019 not reflected in facebook data
# we need to exclude Soignies because it was split into Soignies and La Louvière
df_baseline = df_baseline.loc[~(df_baseline.name == 'Soignies')]
# we need to merge Tournai and Mouscron
df_tournai_mouscron = pd.concat([df_baseline.loc[df_baseline.name == 'Tournai'],
                                 df_baseline.loc[df_baseline.name == 'Mouscron']])
df_tournai_mouscron['name'] = 'Tournai-Mouscron'
df_tournai_mouscron = df_tournai_mouscron.groupby(['name', 'date_time']).agg({'n_baseline': 'sum'})
df_tournai_mouscron = df_tournai_mouscron.reset_index()

# remove original data
df_baseline = df_baseline.loc[~(df_baseline.name == 'Tournai')]
df_baseline = df_baseline.loc[~(df_baseline.name == 'Mouscron')]
df_baseline = pd.concat([df_baseline, df_tournai_mouscron])

df_clean = pd.merge(df_baseline, df_translation, left_on='name', right_on='FR')
df_clean.drop(['FR', 'NL'], axis=1, inplace=True)

df_pop = pd.read_csv("static/csv/ins_pop.csv")
df_pop = df_pop.loc[(df_pop.NIS5 >= 10000) & (df_pop.NIS5 % 1000 == 0) & (df_pop.NIS5 % 10000 != 0)]

df_prop = pd.merge(df_clean, df_pop, left_on='INS', right_on='NIS5')


def to_weekday(x):
    mapping = {
        '2020-04-20': 'Mondays',
        '2020-04-21': 'Tuesdays',
        '2020-04-22': 'Wednesdays',
        '2020-04-23': 'Thursdays',
        '2020-04-24': 'Fridays',
        '2020-04-25': 'Saturdays',
        '2020-04-26': 'Sundays',
    }
    return mapping[x]


df_prop.date_time = df_prop.date_time.apply(to_weekday)


def add_rectangle(fig, x1, y1, x2, y2, color):
    fig.add_shape(
        type="rect",
        x0=x1,
        y0=y1,
        x1=x2,
        y1=y2,
        fillcolor=color,
        opacity=0.5,
        layer="below",
        line_width=0,
    )


def add_text(fig, x, y, text):
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        align='center',
        showarrow=False,
        font=dict(size=16),
        yanchor='top',
    )


@register_plot_for_embedding("facebook-population-proportion")
def population_proportion():
    fig = px.scatter(df_prop, x='POP', y='n_baseline', range_y=[0, 400000], color='name', animation_frame='date_time')
    fig.update_layout(template="plotly_white")
    fig.update_layout(hovermode='x unified')
    return fig


@register_plot_for_embedding("facebook-population-evolution")
def population_evolution():
    fig = px.line(df_population, x='date_time', y='percent_change', color='name')
    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(get_translation(fr="changement du nombre d'utilisateurs", en="change in number of users"))
    )
    fig.update_layout(template="plotly_white")
    fig.update_layout(hovermode='x unified')
    return fig


@register_plot_for_embedding("facebook-moving")
def movement():
    admin_regions = df_movement_range_short.name.unique()
    plots = []
    for a in admin_regions:
        dfa = df_movement_range_short[df_movement_range_short.name == a]
        plot = go.Scatter(x=dfa['date_time'], y=dfa['all_day_bing_tiles_visited_relative_change'].rolling(7).mean(),
                          name=a)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="changement du nombre de tuiles visités", en="change in number of tiles visited"))
    )
    top = 0.5
    bottom = -0.8
    split = 0.4
    add_text(fig, "2020-04-11", top, "Confinement")
    add_rectangle(fig, "2020-03-18", bottom, "2020-05-04", top, "lightsalmon")
    add_rectangle(fig, "2020-10-18", split, df_movement_range.date_time.max(), top, "lightsalmon")
    add_text(fig, "2020-10-18", top, "Confinement")
    add_rectangle(fig, "2020-10-18", bottom, "2020-10-31", split, "yellow")
    add_rectangle(fig, "2020-11-01", bottom, df_movement_range.date_time.max(), split, "lightsalmon")

    fig.update_layout(template="plotly_white")
    fig.update_layout(hovermode='x unified')

    return fig


@register_plot_for_embedding("facebook-staying")
def staying_put():
    admin_regions = df_movement_range_short.name.unique()
    plots = []
    for a in admin_regions:
        dfa = df_movement_range_short[df_movement_range_short.name == a]
        plot = go.Scatter(x=dfa['date_time'], y=dfa['all_day_ratio_single_tile_users'].rolling(7).mean(), name=a)
        plots.append(plot)
    fig = go.Figure(data=plots, layout=go.Layout(barmode='group'))

    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(
            get_translation(fr="proportion d'utilisateurs immobiles", en="fraction of users staying put"))
    )
    top = 0.8
    bottom = 0
    split = 0.74
    add_text(fig, "2020-04-11", top, "Confinement")
    add_rectangle(fig, "2020-03-18", bottom, "2020-05-04", top, "lightsalmon")
    add_rectangle(fig, "2020-10-18", split, df_movement_range.date_time.max(), top, "lightsalmon")
    add_text(fig, "2020-10-18", top, "Confinement")
    add_rectangle(fig, "2020-10-18", bottom, "2020-10-31", split, "yellow")
    add_rectangle(fig, "2020-11-01", bottom, df_movement_range.date_time.max(), split, "lightsalmon")
    fig.update_layout(template="plotly_white")
    fig.update_layout(hovermode='x unified')
    return fig


with open('static/json/admin-units/be-NUTS2016-1.geojson') as json_file:
    geojson_nuts16 = json.load(json_file)
# range_min = df_prov_tot.CASES_PER_THOUSAND.min()
# range_max = df_prov_tot.CASES_PER_THOUSAND.max()
df = df_movement_range_short
dates = df.groupby([df.name]).agg({'date_time': ['max']}).reset_index()
dates.columns = dates.columns.get_level_values(0)

# last_date = "2020-03-03"#dates.date_time.values[0]
# dfl = df[df['date_time']==last_date]

last_date = dates.date_time.values[0]
dfl = dates.merge(df, how='left', left_on=['date_time', 'name'], right_on=['date_time', 'name'])


def map_stayput(column, title):
    fig = px.choropleth_mapbox(dfl, geojson=geojson_nuts16,
                               locations="name",
                               color=column,
                               color_continuous_scale="magma_r",
                               featureidkey="properties.name",
                               center={"lat": 50.641111, "lon": 4.668889},
                               hover_name=column,
                               hover_data=[column, column, "name"],
                               height=600,
                               mapbox_style="carto-positron", zoom=6)
    fig.update_geos(fitbounds="locations")
    fig.layout.coloraxis.colorbar.title = get_translation(fr=title,
                                                          en=title)
    fig.layout.coloraxis.colorbar.titleside = "right"
    fig.layout.coloraxis.colorbar.ticks = "outside"
    fig.layout.coloraxis.colorbar.tickmode = "array"
    fig.update_traces(hovertemplate=gettext(title) + "%{customdata[0]}<br>name:<b>%{customdata[1]}")
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=40, b=0), title=title)
    return fig

@register_plot_for_embedding("facebook-stayputmap")
def map_staying_put():
    return map_stayput("all_day_ratio_single_tile_users", "Fraction Facebook users not moving for 24h at date " + last_date)


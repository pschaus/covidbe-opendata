from graphs import register_plot_for_embedding
from pages import get_translation

import pandas as pd
import geopandas
import plotly.express as px
from flask_babel import get_locale, gettext

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
df_baseline = df_baseline.drop(['n_crisis','percent_change'],axis=1)


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
df_translation.FR =  df_translation.FR.apply(remove_arrondissement)
df_translation.NL =  df_translation.NL.apply(remove_arrondissement)
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
df_tournai_mouscron = df_tournai_mouscron.groupby(['name','date_time']).agg({'n_baseline':'sum'})
df_tournai_mouscron = df_tournai_mouscron.reset_index()

# remove original data
df_baseline = df_baseline.loc[~(df_baseline.name == 'Tournai')]
df_baseline = df_baseline.loc[~(df_baseline.name == 'Mouscron')]
df_baseline = pd.concat([df_baseline,df_tournai_mouscron])

df_clean = pd.merge(df_baseline, df_translation, left_on='name', right_on='FR')
df_clean.drop(['FR','NL'], axis=1, inplace=True)

df_pop = pd.read_csv("static/csv/ins_pop.csv")
df_pop = df_pop.loc[(df_pop.NIS5 >= 10000) & (df_pop.NIS5 % 1000 == 0) & (df_pop.NIS5 % 10000 != 0)]

df_prop = pd.merge(df_clean, df_pop, left_on='INS', right_on='NIS5')

def to_weekday(x):
    mapping = {
        '2020-04-20':'Mondays',
        '2020-04-21':'Tuesdays',
        '2020-04-22':'Wednesdays',
        '2020-04-23':'Thursdays',
        '2020-04-24':'Fridays',
        '2020-04-25':'Saturdays',
        '2020-04-26':'Sundays',
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
    return fig

@register_plot_for_embedding("facebook-population-evolution")
def population_evolution():
    fig = px.line(df_population, x='date_time', y='percent_change', color='name')
    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(get_translation(fr="changement du nombre d'utilisateurs", en="change in number of users"))
    )
    return fig

@register_plot_for_embedding("facebook-moving")
def movement():
    fig = px.line(df_movement_range_short, x='date_time', y='all_day_bing_tiles_visited_relative_change', color='name')
    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(get_translation(fr="changement du nombre de tuiles visités", en="change in number of tiles visited"))
    )
    top = 0.5
    bottom = -0.8
    split = 0.4
    add_text(fig, "2020-04-11", top, "Confinement")
    add_text(fig, "2020-06-09", top, "Deconfinement phases")
    add_text(fig, "2020-05-07", split, "1A")
    add_text(fig, "2020-05-14", split, "1B")
    add_text(fig, "2020-05-29", split, "2")
    add_text(fig, "2020-06-20", split, "3")
    add_text(fig, "2020-07-07", split, "4")
    add_rectangle(fig, "2020-03-18", bottom, "2020-05-04", top, "lightsalmon")
    add_rectangle(fig, "2020-05-04", split, df_movement_range.date_time.max(), top, "darkgreen")
    add_rectangle(fig, "2020-05-04", bottom, "2020-05-11", split, "khaki")
    add_rectangle(fig, "2020-05-11", bottom, "2020-05-18", split, "lightgreen")
    add_rectangle(fig, "2020-05-18", bottom, "2020-06-08", split, "mediumseagreen")
    add_rectangle(fig, "2020-06-08", bottom, "2020-07-01", split, "seagreen")
    add_rectangle(fig, "2020-07-01", bottom, "2020-07-15", split, "green")
    add_text(fig, "2020-10-18", top, "Pre-confinement")
    add_rectangle(fig, "2020-10-18", bottom, df_movement_range.date_time.max(), split, "yellow")
    return fig

@register_plot_for_embedding("facebook-staying")
def staying_put():
    fig = px.line(df_movement_range_short, x='date_time', y='all_day_ratio_single_tile_users', color='name')
    fig.update_layout(
        xaxis_title="date",
        yaxis_title=gettext(get_translation(fr="proportion d'utilisateurs immobiles", en="fraction of users staying put"))
    )
    top = 0.8
    bottom = 0
    split = 0.74
    add_text(fig, "2020-04-11", top, "Confinement")
    add_text(fig, "2020-06-09", top, "Deconfinement phases")
    add_text(fig, "2020-05-07", split, "1A")
    add_text(fig, "2020-05-14", split, "1B")
    add_text(fig, "2020-05-29", split, "2")
    add_text(fig, "2020-06-20", split, "3")
    add_text(fig, "2020-07-07", split, "4")
    add_rectangle(fig, "2020-03-18", bottom, "2020-05-04", top, "lightsalmon")
    add_rectangle(fig, "2020-05-04", split, df_movement_range.date_time.max(), top, "darkgreen")
    add_rectangle(fig, "2020-05-04", bottom, "2020-05-11", split, "khaki")
    add_rectangle(fig, "2020-05-11", bottom, "2020-05-18", split, "lightgreen")
    add_rectangle(fig, "2020-05-18", bottom, "2020-06-08", split, "mediumseagreen")
    add_rectangle(fig, "2020-06-08", bottom, "2020-07-01", split, "seagreen")
    add_rectangle(fig, "2020-07-01", bottom, df_movement_range.date_time.max(), split, "green")
    return fig

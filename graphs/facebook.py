from graphs import register_plot_for_embedding

import pandas as pd
import geopandas
import plotly.express as px

df_population = pd.read_csv('static/csv/facebook/population.csv')

df_baseline = df_population.loc[(df_population.date_time >= '2020-04-20') & (df_population.date_time < '2020-04-27')]
df_baseline.drop(['n_crisis','percent_change'],inplace=True,axis=1)


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
df_translation['NIS3'] = df_translation.apply(lambda x: x['INS'] // 1000, axis=1)
df_translation.FR =  df_translation.FR.apply(remove_arrondissement)
df_translation.NL =  df_translation.NL.apply(remove_arrondissement)
df_translation.drop(['INS', 'Langue'], axis=1, inplace=True)

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

df_pop = pd.read_csv("static/csv/ins_pop.csv", dtype={"NIS5": str})
df_pop['NIS3'] = df_pop.apply(lambda x: x['NIS5'][:2], axis=1)
df3_pop = df_pop.groupby([df_pop.NIS3]).agg({'POP': ['sum']}).reset_index()
df3_pop.columns = df3_pop.columns.get_level_values(0)
df3_pop['NIS3'] = df3_pop['NIS3'].astype(int)

df_prop = pd.merge(df_clean, df3_pop)

@register_plot_for_embedding("facebook-population-proportion")
def population_proportion():
    fig = px.scatter(df_prop, x='POP', y='n_baseline', range_y=[0, 400000], color='name', animation_frame='date_time')
    return fig

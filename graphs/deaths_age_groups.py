import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)




@register_plot_for_embedding("deaths_per_age_group_param")
def age_groups_death():
    """
    bar plot age groups cases
    """
    # ---------bar plot age groups death---------------------------
    barmode = 'stack' #group
    idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
    # bar plot with bars per age groups
    bars_age_groups_deaths = []
    age_groups = sorted(df_mortality.AGEGROUP.unique())
    for ag in age_groups:
        df_ag = df_mortality.loc[df_mortality['AGEGROUP'] == ag]
        df_ag = df_ag.groupby(['DATE']).agg({'DEATHS': 'sum'})
        df_ag.index = pd.DatetimeIndex(df_ag.index)
        df_ag = df_ag.reindex(idx, fill_value=0)
        bars_age_groups_deaths.append(go.Bar(
            x=df_ag.index,
            y=df_ag['DEATHS'],
            name=ag
        ))

    fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths,
                                      layout=go.Layout(barmode='group'), )
    fig_age_groups_deaths.update_layout(template="plotly_white", height=500, barmode=barmode,margin=dict(l=0, r=0, t=30, b=0), title=gettext("Deaths per day per age group"))

    return fig_age_groups_deaths


@register_plot_for_embedding("deaths_per_age_group_pie")
def age_groups_death_pie():

    region_age = df_mortality.groupby(['REGION', 'AGEGROUP']).agg({'DEATHS': 'sum'})
    total_age = df_mortality.groupby(['AGEGROUP']).agg({'DEATHS': 'sum'})

    fig_age_groups_deaths_pie = make_subplots(rows=2, cols=2,
                                              specs=[[{'type': 'domain'}, {'type': 'domain'}],
                                                     [{'type': 'domain'}, {'type': 'domain'}]],
                                              subplot_titles=[
                                                  gettext("Belgium"),
                                                  gettext('Wallonia'),
                                                  gettext('Flanders'),
                                                  gettext("Brussels")
                                              ],
                                              horizontal_spacing=0.01, vertical_spacing=0.2)

    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=total_age['DEATHS'].index.values, values=total_age['DEATHS'], name=gettext("Total"), sort=False, textposition="inside"),
        1, 1)
    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=region_age['DEATHS']['Wallonia'].index.values, values=region_age['DEATHS']['Wallonia'].values, name=gettext("Wallonia"), sort=False,
               textposition="inside"),
        1, 2)
    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=region_age['DEATHS']['Flanders'].index.values, values=region_age['DEATHS']['Flanders'].values, name=gettext("Flanders"), sort=False,
               textposition="inside"),
        2, 1)
    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=region_age['DEATHS']['Brussels'].index.values, values=region_age['DEATHS']['Brussels'].values, name=gettext("Brussels"), sort=False,
               textposition="inside"),
        2, 2)

    fig_age_groups_deaths_pie.update_layout(height=600)

    return fig_age_groups_deaths_pie



@register_plot_for_embedding("deaths_per_age_group_pie")
def age_groups_death_first_wave():

    total_age = df_mortality.groupby(['AGEGROUP']).agg({'DEATHS': 'sum'})

    fig_age_groups_deaths_pie = fig = go.Figure()

    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=total_age['DEATHS'].index.values, values=total_age['DEATHS'], name=gettext("Total"), sort=False, textposition="inside"),
        1, 1)


    return fig_age_groups_deaths_pie




df_first_wave = df_mortality[df_mortality.DATE >= '2020-03-10']
df_first_wave = df_first_wave[df_first_wave.DATE <= '2020-06-01']
df_2nd_wave = df_mortality[df_mortality.DATE >= '2020-09-01']

tot1st = sum(df_first_wave.DEATHS.values)
tot2nd = sum(df_2nd_wave.DEATHS.values)

def waves_comparison():
    df_first_wave = df_mortality[df_mortality.DATE >= '2020-03-10']
    df_first_wave = df_first_wave[df_first_wave.DATE <= '2020-06-01']
    df_2nd_wave = df_mortality[df_mortality.DATE >= '2020-09-01']

    tot1st = sum(df_first_wave.DEATHS.values)
    tot2nd = sum(df_2nd_wave.DEATHS.values)

    # -----------------
    total_age = df_first_wave.groupby(['AGEGROUP']).agg({'DEATHS': 'sum'})
    labels = total_age['DEATHS'].index.values

    fig_age_groups_deaths_pie = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                                              subplot_titles=['1st wave (March-June) tot=' + str(tot1st),
                                                              '2nd wave (Sept-Now) tot=' + str(tot2nd)])


    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=labels, values=total_age['DEATHS'], name=gettext("Total"), sort=True, textposition="inside"), 1,
        1)

    # ---------------------
    total_age = df_2nd_wave.groupby(['AGEGROUP']).agg({'DEATHS': 'sum'})
    labels = total_age['DEATHS'].index.values
    fig_age_groups_deaths_pie.add_trace(
        go.Pie(labels=labels, values=total_age['DEATHS'], name=gettext("Total"), sort=True, textposition="inside"), 1,
        2)

    return fig_age_groups_deaths_pie
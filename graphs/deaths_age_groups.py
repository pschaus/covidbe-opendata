import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding

df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)




@register_plot_for_embedding("age_groups_death_covid")
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
        bars_age_groups_deaths.append(go.Scatter(
            x=df_ag.index,
            y=df_ag['DEATHS'],
            name=ag,
            legendgroup = ag, stackgroup = 'one', line = dict(width=0.5),
            mode = 'lines',
            groupnorm = ""
        ))

    fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths)
    fig_age_groups_deaths.update_layout(template="plotly_white", height=500, barmode=barmode,margin=dict(l=0, r=0, t=30, b=0), title=gettext("Deaths per day per age group"))
    fig_age_groups_deaths.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                buttons=list([
                    dict(
                        args=[{"groupnorm": ""}],
                        label="absolute",
                        method="restyle"
                    ),
                    dict(
                        args=[{"groupnorm": "percent"}],
                        label="percent",
                        method="restyle"
                    )
                ]),
            ),
        ])

    return fig_age_groups_deaths


def df_avg_age_death():
    df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)

    age_group_weight_min = {'0-24': 0, '25-44': 25, '45-64': 45, '65-74': 65, '75-84': 75, '85+': 85}
    age_group_weight_max = {'0-24': 24, '25-44': 44, '45-64': 64, '65-74': 74, '75-84': 84, '85+': 90}

    df_mortality['weight_min'] = df_mortality['AGEGROUP'].map(age_group_weight_min)
    df_mortality['weight_max'] = df_mortality['AGEGROUP'].map(age_group_weight_max)



    df_mortality['weighteddeaths_min'] = df_mortality['weight_min'] * df_mortality['DEATHS']
    df_mortality['weighteddeaths_max'] = df_mortality['weight_max'] * df_mortality['DEATHS']
    df_avg_ag = df_mortality.groupby([df_mortality.DATE]).agg(
        {'DEATHS': ['sum'], 'weighteddeaths_min': ['sum'], 'weighteddeaths_max': ['sum']}).reset_index()
    df_avg_ag.columns = df_avg_ag.columns.get_level_values(0)
    df_avg_ag['avg_age_min'] = df_avg_ag['weighteddeaths_min'] / df_avg_ag['DEATHS']
    df_avg_ag['avg_age_max'] = df_avg_ag['weighteddeaths_max'] / df_avg_ag['DEATHS']

    return df_avg_ag


df_avg_death = df_avg_age_death()


@register_plot_for_embedding("average_age_covid_deaths")
def average_age_death():
    fig = go.Figure()

    y_min = df_avg_death['weighteddeaths_min'].rolling(14, center=True).sum() / df_avg_death['DEATHS'].rolling(14,
                                                                                                               center=True).sum()
    y_max = df_avg_death['weighteddeaths_max'].rolling(14, center=True).sum() / df_avg_death['DEATHS'].rolling(14,

                                                                                                               center=True).sum()
    x = df_avg_death.DATE

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y_min,
        fill=None,
        mode='lines',
        line_color='indigo',
        name="lower-bound"
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=y_max,
        fill='tonexty',  # fill area between trace0 and trace1
        name="upper-bound",
        mode='lines', line_color='indigo'))

    fig.update_layout(template="plotly_white")
    fig.update_layout(title='Average age of covid deaths Belgium',
                      xaxis_title='Week',
                      yaxis_title='Age')
    fig.update_layout(yaxis=dict(range=[0, 90]))

    return fig


@register_plot_for_embedding("regions_death_covid")
def region_death_covid():
    """
    bar plot age groups cases
    """
    # ---------bar plot age groups death---------------------------

    df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)

    barmode = 'stack'  # group
    idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
    # bar plot with bars per age groups
    bars_age_groups_deaths = []
    regions = sorted(df_mortality.REGION.unique())
    for r in regions:
        df_r = df_mortality.loc[df_mortality['REGION'] == r]
        df_r = df_r.groupby(['DATE']).agg({'DEATHS': 'sum'})
        df_r.index = pd.DatetimeIndex(df_r.index)
        df_r = df_r.reindex(idx, fill_value=0)
        bars_age_groups_deaths.append(go.Scatter(
            x=df_r.index,
            y=df_r['DEATHS'],
            name=r,
            showlegend=True,
            mode='lines', groupnorm="",
            stackgroup='two', line=dict(width=0.5)
        ))

    fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths,
                                      layout=go.Layout(barmode='group'), )
    fig_age_groups_deaths.update_layout(template="plotly_white", height=500, barmode=barmode,
                                        margin=dict(l=0, r=0, t=30, b=0), title=gettext("Deaths per region"))

    return fig_age_groups_deaths


@register_plot_for_embedding("regions_death_covid")
def region_covid_death_per_habitant():
    df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv', keep_default_na=False)
    barmode = 'stack'  # group
    idx = pd.date_range(df_mortality.DATE.min(), df_mortality.DATE.max())
    # bar plot with bars per age groups
    bars_age_groups_deaths = []
    regions = sorted(df_mortality.REGION.unique())

    pop = {'Brussels': 1218255, 'Flanders': 6629143, 'Wallonia': 3645243}

    for r in regions:
        df_r = df_mortality.loc[df_mortality['REGION'] == r]
        df_r = df_r.groupby(['DATE']).agg({'DEATHS': 'sum'})
        df_r.index = pd.DatetimeIndex(df_r.index)
        df_r = df_r.reindex(idx, fill_value=0)

        plot = go.Scatter(x=df_r.index, y=(100000 * df_r['DEATHS'] / pop[r]).rolling(7,center=True).mean(), name=r)

        bars_age_groups_deaths.append(plot)

    fig = go.Figure(data=bars_age_groups_deaths,
                    layout=go.Layout(barmode='group'), )
    fig.update_layout(template="plotly_white", height=500, barmode=barmode, margin=dict(l=0, r=0, t=30, b=0), )

    fig.update_layout(template="plotly_white", title="Deaths per 100K inhabitants (avg 7 days)")
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


@register_plot_for_embedding("coviddeaths_per_age_group_pie")
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



@register_plot_for_embedding("coviddeaths_per_age_group_pie")
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

@register_plot_for_embedding("covid-deaths-waves_comparison")
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
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding
from pages import get_translation
import numpy as np
df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')


age_group_pop_dict = {'0-9': 1269068, '10-19': 1300254, '20-29': 1407645, '30-39': 1492290, '40-49': '1504539', '50-59': '1590628',
                  '60-69': 1347139, '70-79': 924291, '80-89': 539390, '90+': 117397}


age_group_dict = {'0-9': '<60', '10-19': '<60', '20-29': '<60', '30-39': '<60', '40-49': '<60', '50-59': '<60',
                  '60-69': '>=60', '70-79': '>=60', '80-89': '>=60', '90+': '>=60'}
df_prov_timeseries['pop_active'] = df_prov_timeseries['AGEGROUP'].map(age_group_dict)


def moving_average(a, n=1) :
    a = a.astype(np.float)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    ret[:n-1] = ret[:n-1]/range(1,n)
    ret[n-1:] = ret[n - 1:] / n
    return ret



def df_avg_age_cases():
    df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')
    age_group_weight = {'0-9': 5, '10-19': 15, '20-29': 25, '30-39': 35, '40-49': 45, '50-59': 55,
                        '60-69': 65, '70-79': 75, '80-89': 85, '90+': 90}

    df_prov_timeseries['pop_active'] = df_prov_timeseries['AGEGROUP'].map(age_group_dict)
    df_prov_timeseries['weight'] = df_prov_timeseries['AGEGROUP'].map(age_group_weight)
    df_prov_timeseries['weightedcases'] = df_prov_timeseries['weight'] * df_prov_timeseries['CASES']
    df_prov = df_prov_timeseries.groupby([df_prov_timeseries.DATE]).agg(
        {'CASES': ['sum'], 'weightedcases': ['sum']}).reset_index()
    df_prov.columns = df_prov.columns.get_level_values(0)
    df_prov['avg_age'] = df_prov['weightedcases'] / df_prov['CASES']
    return df_prov




def df_pop_age_cases():
    df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')
    age_group_pop_dict = {'0-9':   1269068,
                          '10-19': 1300254,
                          '20-29': 1407645,
                          '30-39': 1492290,
                          '40-49': 1504539,
                          '50-59': 1590628,
                          '60-69': 1347139,
                          '70-79':  924291,
                          '80-89':  539390,
                          '90+':    117397}

    df_prov_timeseries['pop'] = df_prov_timeseries['AGEGROUP'].map(age_group_pop_dict)
    df_prov = df_prov_timeseries.groupby(['DATE','AGEGROUP','pop']).agg({'CASES': ['sum']}).reset_index()
    df_prov.columns = df_prov.columns.get_level_values(0)
    return df_prov



df_avg_age = df_avg_age_cases()

@register_plot_for_embedding("incidence_age_group_plot")
def incidence_age_group_plot():
    df_pop = df_pop_age_cases()
    df_pop['incidence'] = df_pop['CASES'] / df_pop['pop'] * 100000

    traces = []
    age_groups = sorted(df_pop.AGEGROUP.unique())
    for idx, ag in enumerate(age_groups):
        df_ag = df_pop.loc[df_pop['AGEGROUP'] == ag]
        trace = dict(x=df_ag.DATE, y=moving_average(df_ag['incidence'].values, 7), mode='lines', name=ag)
        traces.append(trace)

    fig = go.Figure(data=traces)

    # Edit the layout
    fig.update_layout(title='Daily number of cases/100K in the age-group (avg 7 days)',
                      xaxis_title='Date',
                      yaxis_title='Cases/100K')
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


@register_plot_for_embedding("relative_increase_age_group_plot")
def relative_increase_age_group_plot():
    df_pop = df_pop_age_cases()
    df_pop['incidence'] = df_pop['CASES'] / df_pop['pop'] * 100000

    traces = []
    age_groups = sorted(df_pop.AGEGROUP.unique())
    for idx, ag in enumerate(age_groups):
        df_ag = df_pop.loc[df_pop['AGEGROUP'] == ag]

        today = (df_ag['incidence']).rolling(7).mean().values
        oneweekago = today[:-7]
        ratio = (today[7:] / oneweekago * 100) - 100
        dates = df_ag.DATE.values[7:]

        trace = dict(x=dates[5:], y=ratio[5:], mode='lines', name=ag)
        traces.append(trace)

    fig = go.Figure(data=traces)

    # Edit the layout
    fig.update_layout(title='Relative increase/decrease of cases over one week in %',
                      xaxis_title='Date',
                      yaxis_title='% increase/decrease wrt week-1')
    fig.update_layout(template="plotly_white")

    return fig


@register_plot_for_embedding("age_group_cases_relative")
def age_group_cases_relative():
    idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
    bars_age_groups = []
    traces = []
    age_groups = sorted(df_prov_timeseries.AGEGROUP.unique())
    for idx2, ag in enumerate(age_groups):
        df_ag = df_prov_timeseries.loc[df_prov_timeseries['AGEGROUP'] == ag]
        df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
        df_ag.index = pd.DatetimeIndex(df_ag.index)
        df_ag = df_ag.reindex(idx, fill_value=0)
        bars_age_groups.append(go.Bar(
            x=df_ag.index,
            y=df_ag['CASES'],
            name=ag,
            marker_color=px.colors.qualitative.G10[idx2]
        ))
        trace = dict(x=df_ag.index, y=df_ag.CASES, mode='lines',
                     line=dict(width=0.5),
                     stackgroup='one', groupnorm='percent', name=ag)
        traces.append(trace)

    layout = go.Layout(
        showlegend=True,
        yaxis=dict(
            type='linear',
            range=[1, 100],
            dtick=20,
            ticksuffix='%'
        )
    )

    fig = go.Figure(data=traces, layout=layout)

    # Edit the layout
    fig.update_layout(title='Relative Age group percentage of cases',
                      xaxis_title='Date',
                      yaxis_title='Percentage')

    return fig
@register_plot_for_embedding("age_groups_cases")
def age_groups_cases():
    """
    bar plot age groups cases
    """
    df_ag = df_prov_timeseries.groupby(['DATE', 'AGEGROUP']).agg({'CASES': 'sum'}).reset_index()
    df_ag.columns = df_ag.columns.get_level_values(0)
    df_ag = df_ag.sort_values(by="AGEGROUP", axis=0)

    fig = px.bar(df_ag, x="DATE", y="CASES", color="AGEGROUP", title=gettext("Cases per day per age group"))
    fig.update_layout(template="plotly_white")


    return fig


@register_plot_for_embedding("cases_age_groups_pop_active_relative")
def age_groups_pop_active_cases_relative():
    """
    bar plot age groups cases
    """
    idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
    bars_age_groups = []
    age_groups = sorted(df_prov_timeseries.pop_active.unique())

    age_group_pop={'<60': (1269068 + 1300254 + 1407645 + 1492290 + 1504539 + 1590628), '>=60': (1347139 + 924291 + 539390 + 117397)}

    for idx2, ag in enumerate(age_groups):
        df_ag = df_prov_timeseries.loc[df_prov_timeseries['pop_active'] == ag]
        df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
        df_ag.index = pd.DatetimeIndex(df_ag.index)
        df_ag = df_ag.reindex(idx, fill_value=0)
        bars_age_groups.append(go.Bar(
            x=df_ag.index,
            y=df_ag['CASES']/age_group_pop[ag],
            name=ag,
            marker_color=px.colors.qualitative.G10[idx2]
        ))
        bars_age_groups.append(
            go.Scatter(x=df_ag.index, y=moving_average((df_ag['CASES']/age_group_pop[ag]).values, 7), name=(ag + " avg 7 days")))
    fig_age_groups_cases = go.Figure(data=bars_age_groups)
    fig_age_groups_cases.update_layout(template="plotly_white", height=500,
                                       margin=dict(l=0, r=0, t=30, b=0), title=gettext("Cases per day per age group"))

    return fig_age_groups_cases



@register_plot_for_embedding("cases_age_groups_pop_active")
def age_groups_pop_active_cases():
    """
    bar plot age groups cases
    """
    idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
    bars_age_groups = []
    age_groups = sorted(df_prov_timeseries.pop_active.unique())

    for idx2, ag in enumerate(age_groups):
        df_ag = df_prov_timeseries.loc[df_prov_timeseries['pop_active'] == ag]
        df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
        df_ag.index = pd.DatetimeIndex(df_ag.index)
        df_ag = df_ag.reindex(idx, fill_value=0)
        col = px.colors.qualitative.G10[idx2]
        bars_age_groups.append(go.Bar(
            x=df_ag.index,
            y=df_ag['CASES'],
            name=ag,
            marker_color = col,legendgroup = ag, showlegend = True
        ))
        bars_age_groups.append(
            go.Scatter(x=df_ag.index, y=moving_average(df_ag['CASES'].values, 7),
                       name=ag, marker_color = col, legendgroup = ag, showlegend = False))
    fig_age_groups_cases = go.Figure(data=bars_age_groups)
    fig_age_groups_cases.update_layout(template="plotly_white", height=500,
                                       margin=dict(l=0, r=0, t=30, b=0),
                                       title=gettext("Cases per day per age group"))

    fig_age_groups_cases.update_layout(
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


    return fig_age_groups_cases


@register_plot_for_embedding("average_age_cases")
def average_age_cases():
    fig = px.line(df_avg_age, x='DATE', y='avg_age')
    fig.update_layout(template="plotly_white", height=500,
                                       margin=dict(l=0, r=0, t=30, b=0), title=gettext("Average age of cases"))
    return fig


@register_plot_for_embedding("cases_age_groups_pop_active_hypothetical")
def age_groups_pop_active_hypothetical():
    df = df_prov_timeseries
    df_young_reworked = df.loc[(df.pop_active == '>=60') & (df['DATE'] < '2020-06-22')].copy()
    df_young_reworked['CASES'] = df_young_reworked['CASES'].apply(lambda x: x * 7.14)
    df_young_reworked['pop_active'] = '<60'
    df_young = df.loc[(df.pop_active == '<60') & (df['DATE'] >= '2020-06-22')]
    df_old = df.loc[(df.pop_active == '>=60')]

    df_concat = pd.concat([df_young_reworked, df_young, df_old])

    idx = pd.date_range(df_concat.DATE.min(), df_concat.DATE.max())
    bars_age_groups = []
    age_groups = sorted(df_concat.pop_active.unique())
    for idx2, ag in enumerate(age_groups):
        df_ag = df_concat.loc[df_concat['pop_active'] == ag]
        df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
        df_ag.index = pd.DatetimeIndex(df_ag.index)
        df_ag = df_ag.reindex(idx, fill_value=0)
        bars_age_groups.append(go.Bar(
            x=df_ag.index,
            y=df_ag['CASES'],
            name=ag,
            marker_color=px.colors.qualitative.G10[idx2]
        ))


    fig_age_groups_cases = go.Figure(data=bars_age_groups)
    fig_age_groups_cases.update_layout(template="plotly_white", height=500,
                                       margin=dict(l=0, r=0, t=30, b=0), title=get_translation(fr="Nombre de case par groupe d'age (corrigé, voir hypothèses)",en="Number of cases per age group  (corrected, see hypothesises)"))

    return fig_age_groups_cases






@register_plot_for_embedding("cases_age_groups_pie")
def age_groups_cases_pie():
    region_age = df_prov_timeseries.groupby(['REGION', 'AGEGROUP']).agg({'CASES': 'sum'})
    total_age = df_prov_timeseries.groupby(['AGEGROUP']).agg({'CASES': 'sum'})

    labels = sorted(df_prov_timeseries.AGEGROUP.unique())

    fig_age_groups_cases_pie = make_subplots(rows=2, cols=2,
                                             specs=[[{'type': 'domain'}, {'type': 'domain'}],
                                                    [{'type': 'domain'}, {'type': 'domain'}]],
                                             subplot_titles=[
                                                 gettext('Wallonia'),
                                                 gettext('Flanders'),
                                                 gettext("Brussels"),
                                                 gettext("Belgium")
                                             ],
                                             horizontal_spacing=0.01, vertical_spacing=0.2)
    fig_age_groups_cases_pie.add_trace(
        go.Pie(labels=labels, values=region_age['CASES']['Wallonia'].values, name=gettext("Wallonia"), sort=False,
               textposition="inside"),
        1, 1)
    fig_age_groups_cases_pie.add_trace(
        go.Pie(labels=labels, values=region_age['CASES']['Flanders'].values, name=gettext("Flanders"), sort=False,
               textposition="inside"),
        1, 2)
    fig_age_groups_cases_pie.add_trace(
        go.Pie(labels=labels, values=region_age['CASES']['Brussels'].values, name=gettext("Brussels"), sort=False,
               textposition="inside"),
        2, 1)
    fig_age_groups_cases_pie.add_trace(
        go.Pie(labels=labels, values=total_age['CASES'], name=gettext("Total"), sort=False, textposition="inside"),
        2, 2)

    fig_age_groups_cases_pie.update_layout(
        title_text=gettext("Cases per age group, per region"),
        margin=dict(l=0, r=0, t=60, b=0)
    )

    return fig_age_groups_cases_pie

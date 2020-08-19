import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

from graphs import register_plot_for_embedding
from pages import get_translation

df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')

age_group_dict = {'0-9': '<60', '10-19': '<60', '20-29': '<60', '30-39': '<60', '40-49': '<60', '50-59': '<60',
                  '60-69': '>=60', '70-79': '>=60', '80-89': '>=60', '90+': '>=60'}
df_prov_timeseries['pop_active'] = df_prov_timeseries['AGEGROUP'].map(age_group_dict)

@register_plot_for_embedding("cases_age_groups")
def age_groups_cases():
    """
    bar plot age groups cases
    """
    idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
    bars_age_groups = []
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
    fig_age_groups_cases = go.Figure(data=bars_age_groups)
    fig_age_groups_cases.update_layout(template="plotly_white", height=500, barmode="stack",
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
        bars_age_groups.append(go.Bar(
            x=df_ag.index,
            y=df_ag['CASES'],
            name=ag,
            marker_color=px.colors.qualitative.G10[idx2]
        ))
    fig_age_groups_cases = go.Figure(data=bars_age_groups)
    fig_age_groups_cases.update_layout(template="plotly_white", height=500,
                                       margin=dict(l=0, r=0, t=30, b=0), title=gettext("Cases per day per age group"))
    return fig_age_groups_cases



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

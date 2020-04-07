import json
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px



# ---------bar plot age groups cases---------------------------
from plotly.subplots import make_subplots

df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')

idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
# bar plot with bars per age groups
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
fig_age_groups_cases.update_layout(template="plotly_white", height=500, barmode="stack", margin=dict(l=0, r=0, t=30, b=0), title="Cases per day per age group")


# ------------- pie (cases per region per age group) -----------

region_age = df_prov_timeseries.groupby(['REGION', 'AGEGROUP']).agg({'CASES': 'sum'})
total_age = df_prov_timeseries.groupby(['AGEGROUP']).agg({'CASES': 'sum'})

labels = sorted(df_prov_timeseries.AGEGROUP.unique())

fig_age_groups_cases_pie = make_subplots(rows=2, cols=2,
                                         specs=[[{'type': 'domain'}, {'type': 'domain'}],
                                                [{'type': 'domain'}, {'type': 'domain'}]],
                                         subplot_titles=['Wallonia', 'Flanders', "Brussels", "Belgium"],
                                         horizontal_spacing=0.01, vertical_spacing=0.2)
fig_age_groups_cases_pie.add_trace(
    go.Pie(labels=labels, values=region_age['CASES']['Wallonia'].values, name="Wallonia", sort=False,
           textposition="inside"),
    1, 1)
fig_age_groups_cases_pie.add_trace(
    go.Pie(labels=labels, values=region_age['CASES']['Flanders'].values, name="Flanders", sort=False,
           textposition="inside"),
    1, 2)
fig_age_groups_cases_pie.add_trace(
    go.Pie(labels=labels, values=region_age['CASES']['Brussels'].values, name="Brussels", sort=False,
           textposition="inside"),
    2, 1)
fig_age_groups_cases_pie.add_trace(
    go.Pie(labels=labels, values=total_age['CASES'], name="Total", sort=False, textposition="inside"),
    2, 2)

fig_age_groups_cases_pie.update_layout(
    title_text="Cases per age group, per region",
    margin=dict(l=0, r=0, t=60, b=0)
)

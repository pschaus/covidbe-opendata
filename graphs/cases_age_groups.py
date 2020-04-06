import json
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px



# ---------bar plot age groups cases---------------------------

df_prov_timeseries = pd.read_csv('static/csv/be-covid-provinces.csv')

idx = pd.date_range(df_prov_timeseries.DATE.min(), df_prov_timeseries.DATE.max())
# bar plot with bars per age groups
bars_age_groups = []
age_groups = sorted(df_prov_timeseries.AGEGROUP.unique())
for ag in age_groups:
    df_ag = df_prov_timeseries.loc[df_prov_timeseries['AGEGROUP'] == ag]
    df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
    df_ag.index = pd.DatetimeIndex(df_ag.index)
    df_ag = df_ag.reindex(idx, fill_value=0)
    bars_age_groups.append(go.Bar(
        x=df_ag.index,
        y=df_ag['CASES'],
        name=ag
    ))
fig_age_groups_cases = go.Figure(data=bars_age_groups,
                                 layout=go.Layout(barmode='group'), )
fig_age_groups_cases.update_layout(height=900, )
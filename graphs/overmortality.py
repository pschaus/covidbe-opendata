import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from flask_babel import gettext
import colorcet as cc

from graphs import translated_graph

df_mortality = pd.read_csv('static/csv/be-covid-mortality.csv')
df_mortality_ag = df_mortality.groupby(["AGEGROUP"]).agg({"DEATHS": "sum"})
df_mortality_ag_ratio = df_mortality_ag.copy()
df_mortality_ag_ratio.DEATHS /= df_mortality_ag.DEATHS.sum()


df_deaths_2018 = pd.read_csv('static/csv/be-deaths-2018-per-age.csv')
df_deaths_2018_ag = pd.DataFrame({
    'AGEGROUP': ['0-24', '25-44', '45-64', '65-74', '75-84', '85+'],
    'DEATHS': [
        df_deaths_2018.loc[(x <= df_deaths_2018.AGE) & (df_deaths_2018.AGE <= y)].DEATHS.sum()
        for x, y in [(0, 24), (25, 44), (45, 64), (65, 74), (75, 84), (85, 150)]
    ]
})
df_deaths_2018_ag_ratio = df_deaths_2018_ag.copy()
df_deaths_2018_ag_ratio.DEATHS /= df_deaths_2018_ag.DEATHS.sum()
df_resp_deaths_2018_ag = pd.DataFrame({
    'AGEGROUP': ['0-24', '25-44', '45-64', '65-74', '75-84', '85+'],
    'DEATHS': [0.04, 0.15, 2.47, 4.31, 9.41, 14.21]
})



df_mortality_causes_2016 = pd.read_csv('static/csv/be-deaths-2016-per-age-per-cause.csv')
causes = df_mortality_causes_2016.CAUSE.unique()
map_to_covid_agegroups = {  '0-4':  '0-24',   '5-9':  '0-24', '10-14':  '0-24', '15-19':  '0-24', '20-24':  '0-24',
                          '25-29': '25-44', '30-34': '25-44', '35-39': '25-44', '40-44': '25-44',
                          '45-49': '45-64', '50-54': '45-64', '55-59': '45-64', '60-64': '45-64',
                          '65-69': '65-74', '70-74': '65-74',
                          '75-79': '75-84', '80-84': '75-84',
                          '85-89': '85+', '90-94': '85+', '95-99': '85+', '100+': '85+'}
df_mortality_causes_2016.AGEGROUP = df_mortality_causes_2016.AGEGROUP.apply(lambda x: map_to_covid_agegroups[x])
df_mortality_causes_2016 = df_mortality_causes_2016.groupby(["CAUSE", "AGEGROUP", "CAUSEIDX"], as_index=False).agg({"DEATHS": "sum"})
df_mortality_causes_2016.DEATHS /= 365
df_mortality_causes_2016.sort_values(["CAUSEIDX", "AGEGROUP"])


@translated_graph
def daily_deaths():
    agegroups = df_mortality_ag_ratio.index
    td = df_mortality.loc[df_mortality.DATE == "2020-04-06"].groupby(["AGEGROUP"]).agg({"DEATHS": "sum"})
    td = [td.loc[x].DEATHS if x in td.index else 0 for x in agegroups]
    fig = go.Figure(data=[
        go.Bar(name='Deaths Covid-19 2020-04-06', x=agegroups, y=td),
        go.Bar(name='Mean deaths per day 2018', x=agegroups, y=df_deaths_2018_ag.DEATHS/365)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.layout.xaxis.title = "Age group"
    fig.layout.yaxis.title = "Number of deaths per day"
    fig.layout.template = "plotly_white"
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal"
        )
    )
    return fig


@translated_graph
def daily_deaths_respiratory():
    agegroups = df_mortality_ag_ratio.index

    td = df_mortality.loc[df_mortality.DATE == "2020-04-06"].groupby(["AGEGROUP"]).agg({"DEATHS": "sum"})
    td = [td.loc[x].DEATHS if x in td.index else 0 for x in agegroups]
    overmortality_a = td - df_resp_deaths_2018_ag.DEATHS
    overmortality_a.loc[overmortality_a < 0] = 0

    fig = go.Figure(data=[
        go.Bar(name='Deaths Covid-19 2020-04-06', x=agegroups, y=td, offsetgroup=0,
               hovertemplate="%{y}<extra>COVID-19 Deaths %{x}</extra>"
               ),
        go.Bar(name='Mean respiratory-related deaths per day (2016)',
               x=agegroups, y=df_resp_deaths_2018_ag.DEATHS, offsetgroup=1,
               hovertemplate="%{y:.1f}<extra>Expected respiratory deaths %{x}</extra>"
               ),
        go.Bar(name='Respiratory-related overmortality estimate 2020-04-06',
               x=agegroups, y=overmortality_a,
               offsetgroup=1,
               base=df_resp_deaths_2018_ag.DEATHS,
               opacity=0.3,
               marker_color='black',
               customdata=overmortality_a,
               hovertemplate="%{customdata:.1f}<extra>Respiratory overmortality %{x}</extra>")
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.layout.title = "Respiratory-related overmortality estimates 2020-04-06"
    fig.layout.xaxis.title = "Age group"
    fig.layout.yaxis.title = "Number of deaths per day"
    fig.layout.template = "plotly_white"
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal"
        )
    )
    return fig


@translated_graph
def overmortality_respiratory_line():
    out = pd.merge(df_mortality.groupby(["DATE", "AGEGROUP"], as_index=False).agg({"DEATHS": "sum"}),
                   df_resp_deaths_2018_ag,
                   left_on='AGEGROUP',
                   right_on='AGEGROUP',
                   how='left')
    out['OVERMORTALITY'] = (out.DEATHS_x - out.DEATHS_y)
    out.loc[out.OVERMORTALITY < 0, 'OVERMORTALITY'] = 0
    out = out.groupby(["DATE"], as_index=False).agg({"OVERMORTALITY": "sum"})

    fig = px.line(out, x="DATE", y="OVERMORTALITY", title='Respiratory-related overmortality for each day')
    fig.layout.xaxis.title = "Date"
    fig.layout.yaxis.title = "Number of deceased"
    fig.layout.template = "plotly_white"
    fig.update_traces(
        hovertemplate="%{y:.1f} persons<extra><b>%{x}</b></extra>"
    )
    return fig


@translated_graph
def overmortality_estimates_repartition():
    covid_mortality_day = df_mortality.loc[df_mortality.DATE == "2020-04-06"].groupby(["AGEGROUP"]).agg(
        {"DEATHS": "sum"})

    tmp = pd.merge(covid_mortality_day, df_mortality_causes_2016.loc[df_mortality_causes_2016.CAUSEIDX == "J00-J99"],
                   left_on="AGEGROUP", right_on="AGEGROUP", how="left")
    tmp["DEATHS"] = tmp.DEATHS_x - tmp.DEATHS_y
    tmp.loc[tmp.DEATHS < 0, 'DEATHS'] = 0
    del tmp["DEATHS_x"]
    del tmp["DEATHS_y"]
    tmp.CAUSE = "Covid-19 overmortality"
    tmp.CAUSEIDX = "X"

    out = pd.concat([df_mortality_causes_2016, tmp], sort=False, ignore_index=True)
    out["PCT"] = 100.0 * out.DEATHS / out.groupby(["AGEGROUP"]).DEATHS.transform("sum")
    out["PCT_CAUSE"] = out.groupby(["CAUSE"]).DEATHS.transform("sum") / out.DEATHS.sum()
    out = out.sort_values(["PCT_CAUSE", "CAUSEIDX", "AGEGROUP"], ascending=[True, True, True])

    def gen_color(idx, is_covid):
        if is_covid:
            return "red"
        r, g, b = cc.glasbey_bw_minc_20_hue_150_280[idx]
        opa = 0.3
        return f"rgba({r * 255 * opa + (1.0 - opa) * 255},{g * 255 * opa + (1.0 - opa) * 255},{b * 255 * opa + (1.0 - opa) * 255},1)"

    colors = {x: gen_color(idx, x == "Covid-19 overmortality") for idx, x in enumerate(out.CAUSE.unique())}

    def gen_bar(cause):

        cause_data = out.loc[out.CAUSE == cause]
        if cause == "Covid-19 overmortality":
            texttemplate = "%{customdata:.2f}%"
        else:
            texttemplate = None

        return go.Bar(name=cause,
                      x=cause_data.AGEGROUP,
                      y=cause_data.DEATHS,
                      marker_color=colors[cause],
                      texttemplate=texttemplate,
                      textposition="inside",
                      customdata=cause_data.PCT,
                      hovertemplate="%{y:.2f} deaths <br>%{customdata:.2f}% <extra>%{x}<br>" + cause + "</extra>"
                      )

    fig = go.Figure(data=[gen_bar(cause) for cause in out.CAUSE.unique()])
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.layout.xaxis.title = "Age group"
    fig.layout.yaxis.title = "Average number of deceased per day"
    fig.layout.template = "plotly_white"
    fig.layout.title = "Mortality taking into account covid-19 overmortality (estimate 2020-04-06), per age group"
    fig.update_layout(legend_orientation="h", legend_y=-0.2, height=700)

    pie_data = out.groupby(["CAUSE", "CAUSEIDX", "PCT_CAUSE"], as_index=False).agg({"DEATHS": "sum"}).sort_values(
        ["PCT_CAUSE"], ascending=False)
    pie = go.Figure(data=[go.Pie(labels=pie_data.CAUSE, values=pie_data.DEATHS, sort=False,
                                 marker_colors=[colors[x] for x in pie_data.CAUSE]
                                 )])
    pie.layout.title = "Mortality taking into account covid-19 overmortality (estimate 2020-04-06), global"
    pie.update_traces(textposition='inside')
    pie.update_layout(legend_orientation="h", height=700)

    return fig, pie

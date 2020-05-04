import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots

import numpy as np
import altair as alt
from pages import get_translation


from datetime import datetime

import pandas

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')



df = pandas.read_csv("static/csv/mortality_statbel.csv",parse_dates=['DT_DATE'], date_parser=dateparse)



df.dropna(thresh=1,inplace=True)

def week(date):
    return date.isocalendar()[1]



df = df[df['DT_DATE'] >= '2019-12-30']


df['week'] = df.apply(lambda x: week(x['DT_DATE']), axis=1)
df_week = df.groupby(['NR_YEAR','week','CD_AGEGROUP'])["MS_NUM_DEATH"].sum().reset_index()
df_week.rename(columns={"MS_NUM_DEATH": "tot","NR_YEAR": "year","CD_AGEGROUP": "age"},inplace=True)

def death_age_groups(barmode="group"):
    """
    bar plot age group death in belgium
    """

    age_groups = ['0-24', '25-44', '45-64', '65-74', '75-84', '85+']
    bars_age_groups_deaths = []

    for ag in age_groups:
        df_ag = df_week.loc[df_week['age'] == ag]
        bars_age_groups_deaths.append(go.Bar(
            x=df_ag.week,
            y=df_ag['tot'],
            name=ag
        ))

    maxw = df_week.loc[df_week['week'].idxmax()]['week']
    fig_age_groups_deaths = go.Figure(data=bars_age_groups_deaths,
                                      layout=go.Layout(barmode=barmode), )

    # Set x-axis title
    fig_age_groups_deaths.update_xaxes(title_text="Week")

    # Set y-axes titles
    fig_age_groups_deaths.update_yaxes(title_text="Total Deaths")

    # Add shape regions
    fig_age_groups_deaths.update_layout(
        shapes=[
            # 1st highlight during Feb 4 - Feb 6
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=10.5,
                y0=0,
                x1=int(maxw) + 0.5,
                y1=100,
                fillcolor="LightBlue",
                opacity=0.5,
                layer="below",
                line_width=0,
            ),
        ]
    )

    fig_age_groups_deaths.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                                        title=gettext("Weekly Total deaths per age group in Belgium 2020 "))
    return fig_age_groups_deaths

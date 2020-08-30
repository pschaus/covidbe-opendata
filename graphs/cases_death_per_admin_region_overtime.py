from datetime import datetime, date

import geopandas
import plotly.express as px
import pandas as pd
import numpy as np
from flask_babel import gettext
from pages import get_translation

from graphs import register_plot_for_embedding


df3_death = pd.read_csv("static/csv/weekly_mortality_statbel_ins3.csv")
df3_cases = pd.read_csv("static/csv/cases_weekly_ins3.csv")

df = pd.merge(df3_death, df3_cases, left_on=['NIS3','WEEK','name','POP'], right_on=['NIS3','WEEK','name','POP'], how='left')
df = df[df['WEEK'] >= 32]

@register_plot_for_embedding("gapminder_case_deats_adminregion")
def gapminder_case_death_admin_region_overtime():
    fig = px.scatter(df, x="DEATH_PER_1000HABITANT", y='CASES_PER_1000HABITANT',
                     animation_frame="WEEK", animation_group="NIS3",
                     size="POP", color="name", hover_name="name", range_x=[0, 0.35], range_y=[0, 1],height=1000,)
    fig.update_layout(title_text="GapMinder Plot: Weekly CASES vs Deaths / 1000 Inhabitants / Admin Region",
                      xaxis_title=get_translation(en="Cases / 1000 Inhabitants",fr="Cas / 1000 habitants"),
                      yaxis_title=get_translation(en="Death / 1000 Inhabitants",fr="Décès / 1000 habitants"))
    return fig





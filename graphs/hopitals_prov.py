import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pages import model_warning, get_translation
import numpy as np

# ---------plot of cases per province------------------------
from flask_babel import gettext

from graphs import register_plot_for_embedding

df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/provinces/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)
range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()

df = pd.read_csv('static/csv/be-covid-provinces-all.csv')


def total_hospi_provinces():
    return px.line(df, x="DATE", y="TOTAL_IN", color="PROVINCE")

def total_icu_provinces():
    return px.line(df, x="DATE", y="TOTAL_IN_ICU", color="PROVINCE")

def total_hospi_new_in_provinces():
    return px.line(df, x="DATE", y="NEW_IN", color="PROVINCE")

def total_hospi_new_out_provinces():
    return px.line(df, x="DATE", y="NEW_OUT", color="PROVINCE")


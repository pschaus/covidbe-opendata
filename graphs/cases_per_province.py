import json
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px



# ---------plot of cases per province------------------------
df_prov_tot = pd.read_csv('static/csv/be-covid-provinces_tot.csv')

with open('static/json/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)

range_min = df_prov_tot.CASES_PER_THOUSAND.min()
range_max = df_prov_tot.CASES_PER_THOUSAND.max()
map_provinces = px.choropleth_mapbox(df_prov_tot, geojson=geojson_provinces,
                                     locations="PROVINCE",
                                     color='CASES_PER_THOUSAND', color_continuous_scale="Viridis",
                                     range_color=(range_min, range_max),
                                     featureidkey="properties.proviso",
                                     center={"lat": 50.85045, "lon": 4.34878},
                                     hover_name="CASES_PER_THOUSAND",
                                     height=900,
                                     mapbox_style="carto-positron", zoom=7)



# ------------------------------------------------------------


barplot_provinces_cases = px.bar(df_prov_tot, y='PROVINCE_NAME', x='CASES_PER_THOUSAND', color='CASES_PER_THOUSAND', orientation='h',color_continuous_scale="Viridis", range_color = (range_min, range_max), hover_name="PROVINCE_NAME")

barplot_provinces_cases.update_layout(title_text='Cases / Thousands of inhabitants',  height=900)
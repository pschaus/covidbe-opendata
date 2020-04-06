import json
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

df_communes_tot = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})
df_communes_timeseries = pd.read_csv('static/csv/be-covid-timeseries.csv')
with open('static/json/be-geojson.json') as json_file:
    geojson_communes = json.load(json_file)

map_communes = px.choropleth_mapbox(df_communes_tot, geojson=geojson_communes,
                                    locations="NIS5",
                                    color='CASES', color_continuous_scale="Viridis",
                                    range_color=(0, 300),
                                    featureidkey="properties.shn",
                                    center={"lat": 50.85045, "lon": 4.34878},
                                    hover_name="CASES",
                                    hover_data=["FR", "NL"],
                                    custom_data=["NIS5"],
                                    height=900,
                                    mapbox_style="carto-positron", zoom=7)


# ---------bar plot cases time series per commune-----------------
def barplot_communes(commune_nis=73006):
    [nis, case, fr, nl] = df_communes_tot.loc[df_communes_tot['NIS5'] == str(commune_nis)].values[0]
    title = title_text = fr + " / " + nl
    fig = go.Figure(
        [go.Bar(x=df_communes_timeseries['DATE'], y=df_communes_timeseries[str(commune_nis)], text='cases')])
    fig.update_layout(title_text=title)
    return fig

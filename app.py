import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


import urllib.request, json

import plotly.express as px

import pandas as pd

df = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

dft = pd.read_csv('static/csv/be-covid-timeseries.csv')

df_prov = pd.read_csv('static/csv/be-covid-provinces_tot.csv')


with open('static/json/be-geojson.json') as json_file:
    geojson_communes = json.load(json_file)

map_cases = px.choropleth_mapbox(df, geojson=geojson_communes,
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


with open('static/json/be-provinces-geojson.json') as json_file:
    geojson_provinces = json.load(json_file)

map_provinces = px.choropleth_mapbox(df_prov, geojson=geojson_provinces,
                                 locations="PROVINCE",
                                 color='CASES', color_continuous_scale="Rainbow",
                                 range_color=(0, 2500),
                                 featureidkey="properties.proviso",
                                 center={"lat": 50.85045, "lon": 4.34878},
                                 hover_name="CASES",
                                 height=900,
                                 mapbox_style="carto-positron", zoom=7)


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(children=[
    html.H1(children='COVID-DATA',),
    html.H2(children='COVID-DATA',id='my-hoverdata'),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='map-communes', figure=map_cases),),
            dbc.Col(dcc.Graph(id='histogram', figure=map_cases),),

        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='map-prov', figure=map_provinces), ),

        ]
    ),

])


@app.callback(
Output('my-hoverdata', 'children'),
[Input('map-communes', 'hoverData')])
def callback_image(hoverData):
    if hoverData == None:
        return "place your mouse on a municipality"
    else:
        idx = hoverData["points"][0]["pointIndex"]
        if df.iloc[[idx]]['FR'].item() != df.iloc[[idx]]['NL'].item():
            return df.iloc[[idx]]['FR']+"     "+df.iloc[[idx]]['NL']+"    cases:"+ str(df.iloc[[idx]]['CASES'].item())
        else:
            return df.iloc[[idx]]['FR'] + "    cases:"+ str(df.iloc[[idx]]['CASES'].item())


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input('map-communes', 'hoverData')])
def callback_barplot(hoverData):
    if hoverData == None:
         return go.Figure([go.Bar(x=dft['DATE'], y=dft[str(73006)])])
    #print(hoverData)
    custom = hoverData['points'][0]['customdata']
    [nis,fr,nl] = custom
    title = title_text=fr+" / "+nl
    fig = go.Figure([go.Bar(x=dft['DATE'], y=dft[str(nis)], text ='cases')])
    fig.update_layout(title_text=title)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

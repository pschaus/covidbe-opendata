import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


import urllib.request, json

import plotly.express as px

import pandas as pd

df = pd.read_csv("static/csv/be-covid-totcases.csv", dtype={"NIS5": str})

dft = pd.read_csv('static/csv/be-covid-timeseries.csv')


with open('static/json/be-geojson.json') as json_file:
    geojson = json.load(json_file)

map_cases = px.choropleth_mapbox(df, geojson=geojson,
                                 locations="NIS5",
                                 color='CASES', color_continuous_scale="Viridis",
                                 range_color=(0, 300),
                                 featureidkey="properties.shn",
                                 center={"lat": 50.85045, "lon": 4.34878},
                                 hover_name="CASES",
                                 hover_data=["FR", "NL"],
                                 custom_data=["NIS5"],
                                 mapbox_style="carto-positron", zoom=7)

#map_cases.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app = dash.Dash(__name__)
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='COVID-DATA',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #html.Div(children='#UCLouvain #INGI Visualization', style={
    #    'textAlign': 'center',
    #    'color': colors['text']
    #}),

    html.Div(
        className="row",
        children=[

            html.Div(
                className="height columns div-map",
                children=[
                    dcc.Graph(id='my-graph', figure=map_cases),
                ]),

            html.Div(
                className="four columns div-hist",
                children=[
                    dcc.Graph(id='histogram', figure=map_cases),
                ]),
        ]),

    html.Div(id='my-hoverdata',
             style={
                 'textAlign': 'center',
                 'color': colors['text'],
                 'font-size': 20
             }
             ),
])


@app.callback(
Output('my-hoverdata', 'children'),
[Input('my-graph', 'hoverData')])
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
    [Input('my-graph', 'hoverData')])
def callback_barplot(hoverData):
    if hoverData == None:
         return go.Figure([go.Bar(x=dft['DATE'], y=dft[str(73006)])])
    print(hoverData)
    nis = hoverData['points'][0]['customdata'][0]
    print(nis)
    return go.Figure([go.Bar(x=dft['DATE'], y=dft[str(nis)])])



if __name__ == '__main__':
    app.run_server(debug=True)

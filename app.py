import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import urllib.request, json

import plotly.express as px

import pandas as pd

df = pd.read_csv("static/csv/be-covid.csv", dtype={"NIS5": str})

with open('static/json/be-geojson.json') as json_file:
    geojson = json.load(json_file)

map_cases = px.choropleth_mapbox(df, geojson=geojson,
                                 locations="NIS5",
                                 color='CASES', color_continuous_scale="Viridis",
                                 range_color=(0, 300),
                                 featureidkey="properties.shn",
                                 center={"lat": 50.85045, "lon": 4.34878},
                                 hover_name="RANGE",
                                 hover_data=["FR", "NL"],
                                 mapbox_style="carto-positron", zoom=7, height=900)

map_cases.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#bubble_chart = px.scatter(px.data.gapminder(), x="gdpPercap", y="lifeExp", animation_frame="year",
#                          animation_group="country",
#                          size="pop", color="country", hover_name="country",
#                          log_x=True,
#                          size_max=45, range_x=[100, 100000], range_y=[25, 90])





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
    html.Div(children='#UCLouvain #INGI Visualization', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    # Column for app graphs and plots
    html.Div(
        className="map",
        children=[
            dcc.Graph(id='my-graph',figure=map_cases),
            #dcc.Graph(figure=bubble_chart)
        ],
    ),

    html.Div(id='my-hoverdata',
             style={
                 'textAlign': 'center',
                 'color': colors['text'],
                 'font-size': 20
             }
             )



])


@app.callback(
Output('my-hoverdata', 'children'),
[Input('my-graph', 'hoverData')])
def callback_image(hoverData):
    if hoverData == None:
        return "place your mouse on a municipality"
    else:
        idx = hoverData["points"][0]["pointIndex"]
        return df.iloc[[idx]]['FR']+" "+df.iloc[[idx]]['NL']+" #cases:"+df.iloc[[idx]]['RANGE']



if __name__ == '__main__':
    app.run_server(debug=True)

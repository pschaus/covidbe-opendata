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
                                 color='CASES_PER_THOUSAND', color_continuous_scale="Viridis",
                                 range_color=(0, 2.8),
                                 featureidkey="properties.proviso",
                                 center={"lat": 50.85045, "lon": 4.34878},
                                 hover_name="CASES_PER_THOUSAND",
                                 height=900,
                                 mapbox_style="carto-positron", zoom=7)



df_prov_all = pd.read_csv('static/csv/be-covid-provinces.csv')
idx = pd.date_range(df_prov_all.DATE.min(), df_prov_all.DATE.max())

# bar plot with bars per age groups
bars_age_groups = []
age_groups = sorted(df_prov_all.AGEGROUP.unique())
for ag in age_groups:
    df_ag = df_prov_all.loc[df_prov_all['AGEGROUP'] == ag]
    df_ag = df_ag.groupby(['DATE']).agg({'CASES': 'sum'})
    df_ag.index = pd.DatetimeIndex(df_ag.index)
    df_ag = df_ag.reindex(idx, fill_value=0)
    bars_age_groups.append(go.Bar(
        x=df_ag.index,
        y=df_ag['CASES'],
        name=ag
    ))
fig_age_groups = go.Figure(data=bars_age_groups,
                                       layout=go.Layout(barmode='group'),)
fig_age_groups.update_layout(height=1000,)


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
    dbc.Row(
        [
            dcc.Graph(id='bar_age_groups',
                      figure=fig_age_groups
                      )
        ]),

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
    [Input('map-communes', 'clickData')])
def callback_barplot(clickData):
    if clickData == None:
         return go.Figure([go.Bar(x=dft['DATE'], y=dft[str(73006)])])
    custom = clickData['points'][0]['customdata']
    [nis,fr,nl] = custom
    title = title_text=fr+" / "+nl
    fig = go.Figure([go.Bar(x=dft['DATE'], y=dft[str(nis)], text ='cases')])
    fig.update_layout(title_text=title)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

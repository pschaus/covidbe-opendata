# Inspired from https://covid19dashboards.com/covid-compare-permillion/
# and https://gist.github.com/gschivley/578c344461100071b7eef158efccce95

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from os.path import isfile
from app import app
from pages import get_translation

import io

import numpy as np
import altair as alt
#config InlineBackend.figure_format = 'retina'

chart_width = 550
chart_height= 400

#hide 
data = pd.read_csv("static/csv/time_series_covid19_confirmed_global.csv", error_bad_lines=False)
data = data.drop(columns=["Lat", "Long"])
data = data.melt(id_vars= ["Province/State", "Country/Region"])
data = pd.DataFrame(data.groupby(['Country/Region', "variable"]).sum())
data.reset_index(inplace=True)  
data = data.rename(columns={"Country/Region": "location", "variable": "date", "value": "total_cases"})
data['date'] =pd.to_datetime(data.date)
data = data.sort_values(by = "date")
data.loc[data.location == "US","location"] = "United States"
data.loc[data.location == "Korea, South","location"] = "South Korea"

data_pwt = pd.read_stata("https://www.rug.nl/ggdc/docs/pwt91.dta")

filter1 = data_pwt["year"] == 2017
data_pop = data_pwt[filter1]
data_pop = data_pop[["country","pop"]]
data_pop.loc[data_pop.country == "Republic of Korea","country"] = "South Korea"
data_pop.loc[data_pop.country == "Iran (Islamic Republic of)","country"] = "Iran"

# per habitant
data_pc = data.copy()
countries = ["China", "Italy", "Spain", "France", "United Kingdom", "Germany", 
             "Portugal", "United States", "Singapore", "South Korea", "Japan", 
             "Brazil", "Iran", 'Netherlands', 'Belgium', 'Sweden', 
             'Switzerland', 'Norway', 'Denmark', 'Austria', 'Slovenia', 'Greece',
             'Cyprus']
data_countries = []
data_countries_pc = []

MIN_DEATHS = 10
filter_min_dead = data_pc.total_cases < MIN_DEATHS
data_pc = data_pc.drop(data_pc[filter_min_dead].index)

# compute per habitant
for i in countries:
    data_pc.loc[data_pc.location == i,"total_cases"] = data_pc.loc[data_pc.location == i,"total_cases"]/float(data_pop.loc[data_pop.country == i, "pop"])

    # get each country time series
filter1 = data_pc["total_cases"] > 1
for i in countries:
    filter_country = data_pc["location"]== i
    data_countries_pc.append(data_pc[filter_country & filter1])
    
    
    
#hide_input
# Stack data to get it to Altair dataframe format
data_countries_pc2 = data_countries_pc.copy()
for i in range(0,len(countries)):
    data_countries_pc2[i] = data_countries_pc2[i].reset_index()
    data_countries_pc2[i]['n_days'] = data_countries_pc2[i].index
    data_countries_pc2[i]['log_cases'] = np.log10(data_countries_pc2[i]["total_cases"])
data_plot = data_countries_pc2[0]
for i in range(1, len(countries)):    
    data_plot = pd.concat([data_plot, data_countries_pc2[i]], axis=0)
data_plot["trend_2days"] = np.log(2)/2*data_plot["n_days"]
data_plot["trend_4days"] = np.log(2)/4*data_plot["n_days"]
data_plot["trend_12days"] = np.log(2)/12*data_plot["n_days"]
data_plot["trend_2days_label"] = "Doubles every 2 days"
data_plot["trend_4days_label"] = "Doubles evey 4 days"
data_plot["trend_12days_label"] = "Doubles every 12 days"


# Plot it using Altair
source = data_plot

scales = alt.selection_interval(bind='scales')
selection = alt.selection_multi(fields=['location'], bind='legend')

base = alt.Chart(source, title = "COVID-19 Deaths Per Million of Inhabitants").encode(
    x = alt.X('n_days:Q', title = "Days passed since reaching 1 case per million"),
    y = alt.Y("log_cases:Q",title = "Log of cases per million"),
    color = alt.Color('location:N', legend=alt.Legend(title="Country", labelFontSize=15, titleFontSize=17),
                     scale=alt.Scale(scheme='tableau20')),
    opacity = alt.condition(selection, alt.value(1), alt.value(0.1))
)

lines = base.mark_line().add_selection(
    scales
).add_selection(
    selection
).properties(
    width=chart_width,
    height=chart_height
)

trend_2d = alt.Chart(source).encode(
    x = "n_days:Q",
    y = alt.Y("trend_2days:Q",  scale=alt.Scale(domain=(0, max(data_plot["log_cases"])))),
).mark_line(color="grey", strokeDash=[3,3])


labels = pd.DataFrame([{'label': 'Doubles every 2 days', 'x_coord': 6, 'y_coord': 4},
                       {'label': 'Doubles every 4 days', 'x_coord': 16, 'y_coord': 3.5},
                       {'label': 'Doubles every 12 days', 'x_coord': 25, 'y_coord': 1.8},
                      ])
trend_label = (alt.Chart(labels)
                    .mark_text(align='left', dx=-55, dy=-15, fontSize=12, color="grey")
                    .encode(x='x_coord:Q',
                            y='y_coord:Q',
                            text='label:N')
                   )

trend_4d = alt.Chart(source).mark_line(color="grey", strokeDash=[3,3]).encode(
    x = "n_days:Q",
    y = alt.Y("trend_4days:Q",  scale=alt.Scale(domain=(0, max(data_plot["log_cases"])))),
)

trend_12d = alt.Chart(source).mark_line(color="grey", strokeDash=[3,3]).encode(
    x = "n_days:Q",
    y = alt.Y("trend_12days:Q",  scale=alt.Scale(domain=(0, max(data_plot["log_cases"])))),
)


plot1= (
(trend_2d + trend_4d + trend_12d + trend_label + lines)
.configure_title(fontSize=20)
.configure_axis(labelFontSize=15,titleFontSize=18)
)
#plot1.show(("../images/covid-permillion-trajectories.pdf"))
#plot1

# Save html as a StringIO object in memory
plot1_html = io.StringIO()
plot1.save(plot1_html, 'html')


#hide_input
label = 'Deaths'
temp = pd.concat([x.copy() for x in data_countries_pc]).loc[lambda x: x.date >= '3/1/2020']

metric_name = f'{label} per Million'
temp.columns = ['Country', 'date', metric_name]
# temp.loc[:, 'month'] = temp.date.dt.strftime('%Y-%m')
temp.loc[:, f'Log of {label} per Million'] = temp[f'{label} per Million'].apply(lambda x: np.log(x))

temp.groupby('Country').last()

def display_cases_per_million():
    return [
    html.H1(get_translation(
            en="""Cases per million""",
            fr="""Cas par million""",)),
    dcc.Markdown(get_translation(
            en="""
                The number of reported cases per million is a lower bound on the actual number of infected persons per million inhabitants. Countries have had different testing capabilities and approaches.
                """,
            fr="""
            Le nombre de cas signalés par million est une limite inférieure du nombre réel de personnes infectées par million d'habitants. Les pays ont eu différentes capacités et approches pour réaliser les tests de dépistages.
            """,
        )),
    html.Iframe(
        id='plot',
        height='500',
        width='1000',
        sandbox='allow-scripts',

        # This is where we pass the html
        srcDoc=plot1_html.getvalue(),

        # Get rid of the border box
        style={'border-width': '0px'}
    )
    ]

def callback_cases_per_million(app):
    return None


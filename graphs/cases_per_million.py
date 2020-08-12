import pandas as pd
import numpy as np
import altair as alt
from pages import get_translation


def lines_cases_per_million():
    """
    bar plot hospitalization
    """

    #chart_width = 550
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
    data_plot["trend_4days"] = np.log10(2)/4*data_plot["n_days"]
    data_plot["trend_12days"] = np.log10(2)/12*data_plot["n_days"]
    data_plot["trend_4days_label"] = "Doubles evey 4 days"
    data_plot["trend_12days_label"] = "Doubles every 12 days"
    
    
    # Plot it using Altair
    source = data_plot
    
    scales = alt.selection_interval(bind='scales')
    selection = alt.selection_multi(fields=['location'], bind='legend')
    
    base = alt.Chart(source, title = get_translation(
                en="COVID-19 Cases Per Million of Inhabitants",
                fr="Cas positifs de Covid-19 par million d\'habitants", 
                )).encode(
        x = alt.X('n_days:Q', title = get_translation(
                en="Days passed since reaching 1 case per million",
                fr="Jours depuis avoir atteint 1 cas positif par million d\'habitants",
                )),
        y = alt.Y("log_cases:Q",title = get_translation(
                en="Log₁₀ of cases per million",
                fr="Log₁₀ des cas par million",
                )),
        color = alt.Color('location:N', legend=alt.Legend(title=get_translation(
                en="Country",
                fr="Pays",
                ), labelFontSize=14, titleFontSize=16),
                         scale=alt.Scale(scheme='tableau20')),
        opacity = alt.condition(selection, alt.value(1), alt.value(0.1))
    )
    
    lines = base.mark_line().add_selection(
        scales
    ).add_selection(
        selection
    ).properties(
        #width=chart_width,
        height=chart_height
    )
    
    labels = pd.DataFrame([{'label': 'Doubles every 4 days', 'x_coord': 36, 'y_coord': 1.8},
                           {'label': 'Doubles every 12 days', 'x_coord': 45, 'y_coord': 0.7},
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
    (trend_4d + trend_12d + trend_label + lines)
    .configure(font='Helvetica Neue')
    .configure_title(fontSize=18, fontWeight='normal')
    .configure_axis(labelFontSize=14,titleFontSize=14, titleFontWeight='normal')
    )
    
    return plot1
    

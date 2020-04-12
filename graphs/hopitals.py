import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from flask_babel import gettext
from plotly.subplots import make_subplots



df_hospi = pd.read_csv('static/csv/be-covid-hospi.csv')


def bar_hospitalization():
    """
    bar plot hospitalization
    """

    newin_dates = df_hospi.groupby(['DATE']).agg({'NEW_IN': 'sum'})
    newin_bar = go.Bar(x=newin_dates.index, y=newin_dates.NEW_IN, name='#New Hospitalized')

    newout_dates = df_hospi.groupby(['DATE']).agg({'NEW_OUT': 'sum'})
    newout_bar = go.Bar(x=newout_dates.index, y=newout_dates.NEW_OUT, name='#New Discharged')

    totin_dates = df_hospi.groupby(['DATE']).agg({'TOTAL_IN': 'sum'})
    totin_bar = go.Bar(x=totin_dates.index, y=totin_dates.TOTAL_IN, name='#Total Hospitalized')

    fig_hospi = go.Figure(data=[newin_bar, newout_bar, totin_bar], layout=go.Layout(barmode='group'), )
    fig_hospi.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=30, b=0),
                            title="Hospitalizations")

    fig_hospi.update_layout(xaxis_title='Day',
                            yaxis_title='Number of / Day')

    return fig_hospi


df_prov = pd.read_csv('static/csv/be-covid-provinces.csv')

# compute number of hospi / case in each province
df_tot_provinces_hospi = df_hospi.groupby(['PROVINCE_NAME']).agg({'NEW_IN': 'sum'})
df_tot_provinces_cases = df_prov.groupby(['PROVINCE_NAME']).agg({'CASES': 'sum'})
df_tot_provinces_hospi["NEW_IN_PER_CASES"] = df_tot_provinces_hospi['NEW_IN']/df_tot_provinces_cases["CASES"] #nombre d'hospi/nombre de cas
df_tot_provinces_hospi.reset_index(level=0, inplace=True)
df_tot_provinces_hospi.sort_values(by=["NEW_IN_PER_CASES"],inplace=True)
range_min = df_tot_provinces_hospi["NEW_IN_PER_CASES"].min()
range_max = df_tot_provinces_hospi["NEW_IN_PER_CASES"].max()



def bar_hospi_per_case_per_province():
    fig = px.bar(df_tot_provinces_hospi,
                 y='PROVINCE_NAME',
                 x='NEW_IN_PER_CASES',
                 color='NEW_IN_PER_CASES',
                 orientation='h',
                 color_continuous_scale="deep",
                 range_color=(range_min, range_max),
                 hover_name="PROVINCE_NAME",
                 labels={'NEW_IN_PER_CASES': 'Total Hospitalisation per positive case'},
                 height=400)
    fig.update_traces(
        hovertemplate=gettext("<b>%{y}</b><br>%{x:.3f} hospitalisation per postive case"),
        textposition='outside',
        texttemplate='%{x:.3f}'
    )
    fig.layout.coloraxis.colorbar.titleside = 'right'
    fig.layout.yaxis.title = ""
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=5, b=0))
    return fig
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
